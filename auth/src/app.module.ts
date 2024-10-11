import { Module } from '@nestjs/common';
import { MongooseModule } from '@nestjs/mongoose';
import { UsersModule } from './users/users.module';
import { AuthModule } from './auth/auth.module';

@Module({
  imports: [
    // -> mongodb://user:password@serviceName:port/dbName(defined on init-mongo.js)
    MongooseModule.forRoot("mongodb://admin:admin@mongo:27017/auth_db"),
    UsersModule,
    AuthModule,
  ],
})
export class AppModule {}
