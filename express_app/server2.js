// server2.js (CommonJS) or server2.mjs (ESM)
import amqp from "amqplib";

const url = "amqp://rabbitmq_user:rabbitmq_password@rabbitmq_service:5672/%2F?frameMax=131072&heartbeat=10";
const queue = process.env.RABBITMQ_QUEUE || "node_testq";
const payload = process.env.RABBITMQ_PAYLOAD || "Hello RabbitMQ";

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

(async () => {
  let conn;
  try {
    console.log("connecting:", url);
    conn = await amqp.connect(url);
    const ch = await conn.createChannel();
    await ch.assertQueue(queue, { durable: false });

    ch.sendToQueue(queue, Buffer.from(payload), { contentType: "text/plain" });
    console.log("sent:", payload);

    const deadline = Date.now() + 5000;
    while (true) {
      const msg = await ch.get(queue, { noAck: false });
      if (msg) { console.log("recv:", msg.content.toString()); ch.ack(msg); break; }
      if (Date.now() > deadline) throw new Error("timeout waiting for message");
      await sleep(200);
    }

    await ch.close(); await conn.close();
    console.log("ok");
  } catch (e) {
    console.error("error:", e.message);
    try { if (conn) await conn.close(); } catch {}
    process.exit(1);
  }
})();
