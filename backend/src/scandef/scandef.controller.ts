import {
  Controller,
  Get,
  Post,
  Body,
  Patch,
  Param,
  Delete,
} from '@nestjs/common';
import { ScandefService } from './scandef.service';
import { CreateScandefDto } from './dto/create-scandef.dto';
import { UpdateScandefDto } from './dto/update-scandef.dto';
import { ApiTags } from '@nestjs/swagger';
import { StartScandefDto } from './dto/start-scandef.dto';

@Controller('scandef')
@ApiTags('Scan Definitions')
export class ScandefController {
  constructor(private readonly scandefService: ScandefService) {}

  @Post()
  create(@Body() createScandefDto: CreateScandefDto) {
    return this.scandefService.create(createScandefDto);
  }

  @Get()
  findAll() {
    return this.scandefService.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.scandefService.findOne(id);
  }

  @Post(':id/start')
  startScanDef(@Param('id') id: string, @Body() payload: StartScandefDto) {
    return this.scandefService.startScan(id, payload.assets);
  }

  @Patch(':id')
  update(@Param('id') id: string, @Body() updateScandefDto: UpdateScandefDto) {
    return this.scandefService.update(id, updateScandefDto);
  }

  @Delete(':id')
  remove(@Param('id') id: string) {
    return this.scandefService.remove(id);
  }
}
