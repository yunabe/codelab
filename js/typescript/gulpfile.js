const { promisify, format } = require('util');
const { watch, series } = require('gulp');
const { exec, spawn } = require('child_process');
const fs = require('fs');

function run(cmd, args) {
  return new Promise((resolve, reject) => {
    const proc = spawn(cmd, args, {
      'stdio': ['ignore', 'inherit', 'inherit']
    });
    proc.on('exit', (code) => {
      if (code == 0) {
        resolve();
      }
      reject(new Error(format('%s failed', cmd)));
    });
  });
}

async function test() {
  await run('tsc', []);
  await run('jasmine', ['--config=jasmine.json']);
}

async function testWatch() {
  if (!fs.existsSync('dist')) {
    fs.mkdirSync('dist');
  }
  watch('dist/**/*.js', function jasmine(cb) {
    exec('jasmine --config=jasmine.json', function(error, stdout, stderr) {
      console.log(`stdout: ${stdout}`);
      console.log(`stderr: ${stderr}`);
      cb()
    });
  });
  spawn('tsc', ['--watch'], {
    'stdio': ['ignore', 'inherit', 'ignore']
  });
}

async function clean() {
  await run('rm', ['-rf', 'dist']);
}

exports['test'] =  test;
exports['test:w'] = testWatch;
exports['clean'] = clean;
