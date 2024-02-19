import { PartialType } from '@nestjs/swagger';
import { CreateScandefDto } from './create-scandef.dto';

export class UpdateScandefDto extends PartialType(CreateScandefDto) {}
