// Native BLE bridge for the Capacitor (Android) build.
// Bundled by esbuild into www/native-ble.js and loaded before the app script,
// where it exposes window.TeporeBLE. The app uses Web Bluetooth on the web and
// this bridge on native — same advertisement shape reaches ingest().
import { BleClient } from '@capacitor-community/bluetooth-le';

function toMapNum(o){ const m = new Map(); if(o) for(const k in o) m.set(parseInt(k, 10), o[k]); return m; }
function toMap(o){ const m = new Map(); if(o) for(const k in o) m.set(k, o[k]); return m; }

window.TeporeBLE = {
  async start(onAdv){
    await BleClient.initialize({ androidNeverForLocation: true });
    await BleClient.requestLEScan({ allowDuplicates: true }, (res) => {
      onAdv({
        device: { id: res.device && res.device.deviceId, name: res.localName || (res.device && res.device.name) },
        rssi: res.rssi,
        manufacturerData: toMapNum(res.manufacturerData),
        serviceData: toMap(res.serviceData),
      });
    });
  },
  async stop(){
    try { await BleClient.stopLEScan(); } catch (_) {}
  },
};
