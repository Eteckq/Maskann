import { Entity, Column, PrimaryColumn, BaseEntity } from 'typeorm';

@Entity()
export class EngineType extends BaseEntity {
  @PrimaryColumn()
  name: string;

  @Column('json')
  options: JSON;

  @Column('json')
  reponse: JSON;

  @Column()
  need_assets: boolean;
}
