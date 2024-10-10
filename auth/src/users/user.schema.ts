import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { HydratedDocument } from 'mongoose';

export type UserDocument = HydratedDocument<User>;

@Schema()
export class User {

  @Prop({unique: true})
  id: number;

  @Prop({required: true, unique: true})
  username: string;
  
  @Prop({required: true, unique: true})
  fullName:string;

  @Prop({required: true})
  password: string;

  @Prop({default: Date.now})
  createdAt: Date;
}

export const UserSchema = SchemaFactory.createForClass(User);