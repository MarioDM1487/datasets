// Assembles www/ for Capacitor from the shared web app (tepore.html).
// Copies tepore.html -> www/index.html, injects the native BLE bundle, and
// copies the manifest. Keeps a single source of truth for the app UI.
const fs = require('fs');
const path = require('path');

const SRC = path.join(__dirname, '..', 'holyiot-beacon-reader');
const WWW = path.join(__dirname, 'www');
fs.mkdirSync(WWW, { recursive: true });

let html = fs.readFileSync(path.join(SRC, 'tepore.html'), 'utf8');
// Load the native bridge before the app's inline script so window.TeporeBLE exists.
html = html.replace('<!--NATIVE_BLE-->', '<script src="native-ble.js"></script>');
fs.writeFileSync(path.join(WWW, 'index.html'), html);

fs.copyFileSync(path.join(SRC, 'tepore.webmanifest'), path.join(WWW, 'tepore.webmanifest'));

if (!fs.existsSync(path.join(WWW, 'native-ble.js'))) {
  console.warn('warning: www/native-ble.js missing — run "npm run build:ble" first');
}
console.log('build-web: www/index.html assembled');
