"""
API views for the equipment app.
"""
import io
import zipfile
from pathlib import Path

from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import UploadedDataset, DataSummary
from .serializers import UploadedDatasetListSerializer, UploadedDatasetDetailSerializer, DataSummarySerializer
from .utils import parse_csv, compute_summary, compute_type_stats_from_raw_data, generate_pdf


@api_view(['GET'])
@permission_classes([AllowAny])
def ensure_csrf(request):
    """Ensure CSRF cookie is set for the frontend (call before first POST)."""
    from django.middleware.csrf import get_token
    get_token(request)
    return Response({'detail': 'ok'})


@api_view(['GET'])
@permission_classes([AllowAny])
def download_app(request):
    """Serve the desktop app as a zip file."""
    project_root = Path(settings.BASE_DIR).parent
    desktop_dir = project_root / 'desktop'
    if not desktop_dir.exists():
        return Response({'error': 'Desktop app not found'}, status=status.HTTP_404_NOT_FOUND)

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file_path in desktop_dir.rglob('*'):
            if file_path.is_file() and '__pycache__' not in str(file_path):
                arcname = file_path.relative_to(desktop_dir.parent)
                zf.write(file_path, arcname)

    buffer.seek(0)
    response = HttpResponse(buffer.read(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="chemical-equipment-visualizer-desktop.zip"'
    return response


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Create a new user. Returns error if username exists or fields missing."""
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {'error': 'Username and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Username already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create_user(username=username, password=password)
    return Response({'id': user.id, 'username': user.username}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def auth_login(request):
    """Authenticate user, call Django login(), return session and token for desktop app."""
    from django.contrib.auth import authenticate

    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {'error': 'Username and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(request, username=username, password=password)
    if user is None:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    login(request, user)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({
        'user_id': user.id,
        'username': user.username,
        'token': token.key,
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def auth_logout(request):
    """Log out the user."""
    try:
        Token.objects.filter(user=request.user).delete()
    except Exception:
        pass
    logout(request)
    return Response({'detail': 'Logged out'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_file(request):
    """
    Receive 'file' in request.FILES, parse CSV, compute summary,
    save UploadedDataset and DataSummary, keep only last 5 datasets.
    """
    if 'file' not in request.FILES:
        return Response(
            {'error': 'No file provided'},
            status=status.HTTP_400_BAD_REQUEST
        )

    uploaded_file = request.FILES['file']
    if not uploaded_file.name.endswith('.csv'):
        return Response(
            {'error': 'File must be a CSV'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        df = parse_csv(uploaded_file)
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': f'Failed to parse CSV: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

    summary_data = compute_summary(df)
    raw_data = df.to_dict(orient='records')

    dataset = UploadedDataset.objects.create(
        user=request.user,
        file_name=uploaded_file.name,
        raw_data=raw_data
    )
    DataSummary.objects.create(
        dataset=dataset,
        total_count=summary_data['total_count'],
        avg_flowrate=summary_data['avg_flowrate'],
        avg_pressure=summary_data['avg_pressure'],
        avg_temperature=summary_data['avg_temperature'],
        type_distribution=summary_data['type_distribution'],
        type_stats=summary_data.get('type_stats', {}),
    )

    # Delete datasets beyond the 5 most recent for THIS user only
    excess = UploadedDataset.objects.filter(user=request.user).order_by('-uploaded_at')[5:]
    for d in excess:
        d.delete()

    return Response({
        'dataset_id': dataset.id,
        'summary': summary_data,
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dataset_list(request):
    """Return list of last 5 datasets (id, file_name, uploaded_at)."""
    datasets = UploadedDataset.objects.filter(user=request.user)[:5]
    serializer = UploadedDatasetListSerializer(datasets, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dataset_detail(request, pk):
    """Return one dataset with its raw_data."""
    try:
        dataset = UploadedDataset.objects.get(pk=pk, user=request.user)
    except UploadedDataset.DoesNotExist:
        return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = UploadedDatasetDetailSerializer(dataset)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def summary_detail(request, pk):
    """Return the DataSummary for a dataset. Fills type_stats from raw_data if missing."""
    try:
        dataset = UploadedDataset.objects.get(pk=pk, user=request.user)
    except UploadedDataset.DoesNotExist:
        return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)
    try:
        summary = dataset.summary
    except DataSummary.DoesNotExist:
        return Response({'error': 'Summary not found'}, status=status.HTTP_404_NOT_FOUND)
    data = DataSummarySerializer(summary).data
    # For older datasets without type_stats, compute from raw_data so charts show avg temp/pressure
    if not data.get('type_stats') and dataset.raw_data:
        data['type_stats'] = compute_type_stats_from_raw_data(dataset.raw_data)
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_pdf(request, pk):
    """Return PDF as attachment."""
    try:
        dataset = UploadedDataset.objects.get(pk=pk, user=request.user)
    except UploadedDataset.DoesNotExist:
        return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)
    try:
        summary = dataset.summary
    except DataSummary.DoesNotExist:
        return Response({'error': 'Summary not found'}, status=status.HTTP_404_NOT_FOUND)

    buffer = generate_pdf(dataset, summary)
    from django.http import HttpResponse
    response = HttpResponse(buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="report_{dataset.file_name}.pdf"'
    return response
