import { BadRequestException, Injectable, NotFoundException, OnModuleInit } from "@nestjs/common";
import { Model } from "mongoose";
import { InjectModel } from "@nestjs/mongoose";
import * as bcrypt from 'bcrypt';
import { User } from "./user.schema";
import { UserDto } from "./user.dto";


@Injectable()
export default class UsersService implements OnModuleInit{

    constructor(
      @InjectModel(User.name) private userModel: Model<User>,
    ){}

    async onModuleInit() {
      const username = 'admin';
      const password = 'admin';
      
      try{
          await this.findUserByUsername(username);        
      }catch(e){
        if (!(e instanceof NotFoundException)){ throw e }
        else{
          await this.createUser(
            {
              username: username,
              password: password,
              fullName:"Admin User",
            } as UserDto
          ); 
        }
      }
    }

    findAll(): Promise<User[]> {
      return this.userModel.find().populate('campus').exec();
    }

    async createUser(userDTO: UserDto): Promise<User>{
      try{
        await this.findUserByUsername(userDTO.username);
        throw new BadRequestException('user already exists');
      }catch (e){
        if (!(e instanceof NotFoundException)){
          throw e
        }
        const salt = await bcrypt.genSalt();
        const hashPassword = await bcrypt.hash(userDTO.password,salt);
        const newUser = new this.userModel({
          username:userDTO.username, 
          fullName:userDTO.fullName, 
          password:hashPassword, 
        })
        return await newUser.save();
      }
    }

    async findUserByUsername(username:string): Promise<User> {
      const user = await this.userModel.findOne({username}).exec();
      if (!user){
        throw new NotFoundException();
      }
      return user;
    }
}