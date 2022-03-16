import 'dotenv/config';
import { Yuna } from './config.js';

import './events/onlineAlert.js';

import './server.js';
Yuna.login(process.env.TOKEN);
