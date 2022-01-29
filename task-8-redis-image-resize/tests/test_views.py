import json
import time

import pytest

ns = "http://127.0.0.1:5000/images/"


def test_whole_cycle(client):
    response = client.post(
        ns,
        data=json.dumps(
            dict(
                image="R0lGODlhEAAOALMAAOazToeHh0tLS/7LZv/0jvb29t/f3//Ub//ge8WSLf/rhf/3kdbW1mxsbP//mf///yH5BAAAAAAALAAAAAAQAA4AAARe8L1Ekyky67QZ1hLnjM5UUde0ECwLJoExKcppV0aCcGCmTIHEIUEqjgaORCMxIC6e0CcguWw6aFjsVMkkIr7g77ZKPJjPZqIyd7sJAgVGoEGv2xsBxqNgYPj/gAwXEQA7",
                size_X=8,
                size_Y=8,
            )
        ),
        content_type="application/json",
    )
    data = json.loads(json.loads(response.data))

    assert (
        "not base64 string"
        in client.post(
            ns,
            data=json.dumps(
                dict(
                    image="nothing here",
                    size_X=8,
                    size_Y=8,
                )
            ),
            content_type="application/json",
        ).get_data(as_text=True)
    )

    assert (
        "height and width must be greater than 0"
        in client.post(
            ns,
            data=json.dumps(
                dict(
                    image="R0lGODlhEAAOALMAAOazToeHh0tLS/7LZv/0jvb29t/f3//Ub//ge8WSLf/rhf/3kdbW1mxsbP//mf///yH5BAAAAAAALAAAAAAQAA4AAARe8L1Ekyky67QZ1hLnjM5UUde0ECwLJoExKcppV0aCcGCmTIHEIUEqjgaORCMxIC6e0CcguWw6aFjsVMkkIr7g77ZKPJjPZqIyd7sJAgVGoEGv2xsBxqNgYPj/gAwXEQA7",
                    size_X=0,
                    size_Y=0,
                )
            ),
            content_type="application/json",
        ).get_data(as_text=True)
    )

    assert "request is being processed" in data["message"]

    url = data["url"]
    time.sleep(2)
    response = client.get(ns + url)
    data = json.loads(json.loads(response.data))

    assert "Invalid url" in client.get(ns + "rawr").get_data(as_text=True)

    assert "Invalid url" in client.delete(ns + "rawr").get_data(as_text=True)

    assert (
        data["image"]
        == "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAAHAAgDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD0SXWlgheFDcrqKfL8hAUyDpn1GfWiiiualhVBWUn95pKpfoj/2Q=="
    )

    assert "Image successfully deleted" in client.delete(ns + url).get_data(
        as_text=True
    )
