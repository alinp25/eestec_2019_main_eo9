const request = require('request');
const Logger = require('tracer').console();
// const socket = require('socket.io-client')('http://172.24.1.100');

const KEY = 'Player_1_Key';
const IP = 'Match_IP'

Logger.log(IP)

// the server ip
const socket = require('socket.io-client')(`http://${IP}`);

function sleep(ms) {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}

class Player {;
  constructor(key) {
    this.position = "left";
    this.secretKey = key;
    this.addKey = this.addKey.bind(this);
    this.playScorpio = this.playScorpio.bind(this);
    this.sendCmd = this.sendCmd.bind(this);
    request.post('http://' + IP + '/get_status', {
      json: {
        key: KEY
      }
    }, (err, res, body) => {
      if (body['player'] == 'p1') {
        this.position = "left";
      } else {
        this.position = "right";
      }
    })
  }

  addKey(body) {
    return {
      key: this.secretKey,
      ...body,
    };
  }


  async sendCmd(cmd, timeout = 100) {
    try {
      // prepateTimeDiff();
      socket.emit('command', this.addKey({
        commands: cmd,
      }));
      // printTimeDiff('socket emit');
      Logger.log('Sending ', cmd);
      await sleep(timeout);
    } catch (e) {
      Logger.error(e);
    }
  }

  async teleportRight() {
    await this.sendCmd({ down: true }, 20);
    await this.sendCmd({ down: false }, 20);
    await this.sendCmd({ right: true }, 20);
    await this.sendCmd({ right: false }, 20);
    await this.sendCmd({ front_kick: true }, 20);
    await this.sendCmd({ front_kick: false });
  }

  async teleportLeft() {
    await this.sendCmd({ down: true }, 20);
    await this.sendCmd({ down: false }, 20);
    await this.sendCmd({ left: true }, 20);
    await this.sendCmd({ left: false }, 20);
    await this.sendCmd({ front_kick: true }, 20);
    await this.sendCmd({ front_kick: false });
  }

  async spearLeft() {
    await this.sendCmd({left: true}, 20);
    await this.sendCmd({left: false}, 20);
    await this.sendCmd({right: true}, 20);
    await this.sendCmd({front_punch: true}, 20);
    await this.sendCmd({right: false}, 20);
    await this.sendCmd({front_punch: false}, 20);
  }

  async spearRight() {
    await this.sendCmd({right: true}, 20);
    await this.sendCmd({right: false}, 20);
    await this.sendCmd({left: true}, 20);
    await this.sendCmd({front_punch: true}, 20);
    await this.sendCmd({left: false}, 20);
    await this.sendCmd({front_punch: false}, 20);
  }

  async takeDownRight() {
    await this.sendCmd({left: true}, 20);
    await this.sendCmd({left: false}, 20);
    await this.sendCmd({right: true}, 20);
    await this.sendCmd({back_kick: true}, 20);
    await this.sendCmd({right: false}, 20);
    await this.sendCmd({back_kick: false}, 20);
  }

  async takeDownLeft() {
    await this.sendCmd({right: true}, 20);
    await this.sendCmd({right: false}, 20);
    await this.sendCmd({left: true}, 20);
    await this.sendCmd({back_kick: true}, 20);
    await this.sendCmd({left: false}, 20);
    await this.sendCmd({back_kick: false}, 20);
  }

  async combo_left() {
    await this.teleportLeft();
    await sleep(350);
    await this.spearRight();
    await sleep(350);
    await this.takeDownRight();
    await sleep(350);
  }

  async combo_right() {
    await this.teleportRight();
    await sleep(350);
    await this.spearLeft();
    await sleep(350);
    await this.takeDownLeft();
    await sleep(350);
  }

  async playScorpio() {
    const { sendPlayerSelect, sendPlayerConfirm, sendCmd } = this;
    setInterval(async () => {
      try {
        Logger.log('new command series');
        while (true) {
          if (this.position == "left") {
            await this.combo_left();
            await sleep(350);
            await this.combo_right();
          } else {
            await this.combo_right();
            await sleep(350);
            await this.combo_left();
          }
        }
        
      } catch (e) {
        Logger.error('Error trying to send commands: ', e);
      }
    }, 3000);
  }
}

// your client key
const p1 = new Player(KEY);
p1.playScorpio();
module.exports = {
  Player,
};
