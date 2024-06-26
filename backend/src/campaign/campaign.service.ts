import { Injectable } from '@nestjs/common';
import { CreateCampaignDto } from './dto/create-campaign.dto';
import { UpdateCampaignDto } from './dto/update-campaign.dto';

@Injectable()
export class CampaignService {
  create(createCampaignDto: CreateCampaignDto) {
    return 'This action adds a new campaign';
  }

  findAll() {
    return `This action returns all campaign`;
  }

  findOne(id: string) {
    return `This action returns a #${id} campaign`;
  }

  update(id: string, updateCampaignDto: UpdateCampaignDto) {
    return `This action updates a #${id} campaign`;
  }

  remove(id: string) {
    return `This action removes a #${id} campaign`;
  }
}
