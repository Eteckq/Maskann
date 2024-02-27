import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { EngineModule } from './engine/engine.module';
import { TypeOrmModule } from '@nestjs/typeorm';
import { ScandefModule } from './scandef/scandef.module';
import { WorkflowModule } from './workflow/workflow.module';
import { CampaignModule } from './campaign/campaign.module';

@Module({
  imports: [
    TypeOrmModule.forRoot({
      type: 'mysql',
      host: 'localhost',
      port: 3306,
      username: 'yoyo',
      password: 'yoyo',
      database: 'engine',
      autoLoadEntities: true,
      synchronize: true,
    }),
    EngineModule,
    ScandefModule,
    WorkflowModule,
    CampaignModule,
  ],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
