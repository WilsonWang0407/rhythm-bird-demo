using System.Collections;
using UnityEngine;
using WebSocketSharp;
using System.Collections.Generic;
using Newtonsoft.Json.Linq;

public class BeatReceiver : MonoBehaviour {
    public Sprite idleSprite;
    public Sprite singSprite;
    public float singDuration = 0.2f;

    private WebSocket ws;
    private SpriteRenderer spriteRenderer;
    private Queue<float> beatQueue = new Queue<float>();
    private float startTime;
    private bool isSinging = false;

    private void Start() {
        spriteRenderer = GetComponent<SpriteRenderer>();

        ws = new WebSocket("ws://localhost:6789");
        ws.OnMessage += (sender, e) => {
            var beatJson = JObject.Parse(e.Data);
            float beatTime = beatJson["beat"].ToObject<float>();
            lock (beatQueue) {
                beatQueue.Enqueue(beatTime);
            }
        };

        ws.Connect();

        startTime = Time.time;

        StartCoroutine(BeatChecker());
    }

    private IEnumerator BeatChecker() {
        while (true) {
            float now = Time.time - startTime;

            lock (beatQueue) {
                if (beatQueue.Count > 0 && now >= beatQueue.Peek()) {
                    beatQueue.Dequeue();
                    if (!isSinging)
                        StartCoroutine(SingAnimation());
                }
            }

            yield return null;
        }
    }

    private IEnumerator SingAnimation() {
        isSinging = true;
        spriteRenderer.sprite = singSprite;
        yield return new WaitForSeconds(singDuration);
        spriteRenderer.sprite = idleSprite;
        isSinging = false;
    }

    private void OnDestroy() {
        if (ws != null && ws.IsAlive) {
            ws.Close();
        }
    }
}