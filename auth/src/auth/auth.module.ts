import { Module } from '@nestjs/common';
import { AuthController } from './auth.controller';
import { AuthService } from './auth.service';
import { JwtModule } from '@nestjs/jwt';

import { UsersModule } from 'src/users/users.module';

@Module({
    imports: [
        JwtModule.register({
            global: true,
            secret: "senhasupersecreta",
            signOptions: { expiresIn: '24h' },
            }),
        UsersModule
    ],
    providers: [AuthService],
    controllers: [AuthController],
    exports: [AuthService],
})
export class AuthModule {}
