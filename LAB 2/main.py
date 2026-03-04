#!/usr/local/bin python3
from client_http import load_config, setup_logging, APIClient

def main():
    cfg = load_config()
    log = setup_logging(cfg["logging"])
    client = APIClient(cfg["api"]["base_url"], cfg["api"]["timeout"], log)

    post = client.get("/posts/1")
    log.info("Post ricevuto: id=%s title=%s", post["id"], post["title"])

    payload = {"title": "foo", "body": "bar", "userId": 1}
    new_post = client.post("/posts", data=payload)
    log.info("Creato nuovo post con id %s", new_post.get("id"))

if __name__ == "__main__":
    main()