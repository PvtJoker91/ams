from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError, ParseError
from rest_framework.response import Response
from rest_framework.views import APIView

from archive.models import ArchiveBox, StorageShelf
from common.services.dossiers import update_dossiers_in_box_status_and_sector
from common.services.statuses import AB_PLACEMENT_AVAILABLE_STATUSES
from logistics.permissions import IsInLogisticsGroup
from logistics.serializers.placement import ABPlacementSerializer


@extend_schema_view(
    put=extend_schema(summary='Place archive box list on storage', tags=['Logistics']),
)
class ABPlacementView(APIView):
    permission_classes = [IsInLogisticsGroup]
    serializer_class = ABPlacementSerializer

    def get_object(self, barcode):
        try:
            return ArchiveBox.objects.get(barcode=barcode)
        except (ArchiveBox.DoesNotExist, ValidationError):
            raise status.HTTP_400_BAD_REQUEST

    def validate_barcodes(self, barcode_list):
        for barcode in barcode_list:
            try:
                ArchiveBox.objects.get(barcode=barcode)
            except (ArchiveBox.DoesNotExist, ValidationError):
                raise status.HTTP_400_BAD_REQUEST
        return True

    def put(self, request, *args, **kwargs):
        data = request.data
        barcode_list = [i['barcode'] for i in data]
        self.validate_barcodes(barcode_list)
        instances = []
        for temp_dict in data:
            barcode = temp_dict['barcode']
            current_sector = temp_dict['current_sector']
            status = temp_dict['status']
            shelf_code = temp_dict['shelf_code']
            storage_address = StorageShelf.objects.get(shelf_code=shelf_code)
            obj = self.get_object(barcode)
            if obj.status in AB_PLACEMENT_AVAILABLE_STATUSES:
                obj.status = status
                obj.current_sector.id = current_sector
                obj.storage_address = storage_address
                obj.save()
                instances.append(obj)
                update_dossiers_in_box_status_and_sector(obj)
            else:
                raise ParseError(
                    f"Archive box {obj.barcode} should not be on this operation. Box current operation is {obj.status}")
        serializer = self.serializer_class(instances, many=True)
        return Response(serializer.data)
