from curl_to_json import parse

def test_for_headers():
    bash_sting = "curl -X POST -H 'Content-Type: application/json' -d '{\"foo\": \"bar\"}' http://example.com"

    assert parse(bash_sting).headers['Content-Type'] == 'application/json'
    assert parse(bash_sting).data == {'foo': 'bar'}


def test_for_multiple_headers():
    assert parse(
        "curl -X POST -H 'Content-Type: application/json' -H 'Authorization: Bearer abc123' -d '{\"foo\": \"bar\"}' http://example.com").headers == {
               'Content-Type': 'application/json', 'Authorization': 'Bearer abc123'}


def test_for_get_method():
    assert parse("curl -X GET http://example.com").request.upper() == "GET"


def test_for_post_method():
    assert parse("curl -X POST http://example.com").request.upper() == "POST"


def test_for_url_with_params():
    assert parse("curl http://example.com?foo=bar&baz=qux").url == "http://example.com?foo=bar&baz=qux"


def test_for_url_with_params_with_post():
    assert parse("curl -X POST http://example.com?foo=bar&baz=qux").url == "http://example.com?foo=bar&baz=qux"


def test_with_data():
    assert parse('curl -d "name=curl" -d "tool=cmdline" https://example.com').data == {'name': 'curl',
                                                                                       'tool': 'cmdline'}


def test_with_data_and_header():
    assert parse(
        "curl -X POST -H 'Content-Type: application/json' -d '{\"foo\": \"bar\"}' http://example.com").data == {
               'foo': 'bar'}


def test_for_http_v2():
    assert parse("curl --http2 -i http://example.com").http2 == True


def test_for_http_v1():
    assert parse("curl http://example.com").http2 == False


def test_for_proxy():
    assert parse("curl --proxy 192.168.1.1:3128 http://example.com").proxy == "http://192.168.1.1:3128"


def test_for_proxy_with_auth():
    assert parse(
        "curl --proxy 192.168.1.1:3128 --proxy-user user:pass http://example.com").proxy == "http://user:pass@192.168.1.1:3128"


def test_for_proxy_with_scheme():
    assert parse("curl --proxy http://192.168.1.1:3128 http://example.com").proxy == "http://192.168.1.1:3128"


def test_for_insecure():
    assert parse("curl --insecure https://example.com").insecure is False


def test_for_url():
    assert parse("curl http://example.com").url == "http://example.com"


def test_for_redirect():
    assert parse("curl --location http://example.com").location is True


def test_for_user_agent():
    assert parse("curl -A 'My User Agent' http://example.com").headers['User-Agent'] == "My User Agent"


def test_for_cookie():
    assert parse("curl --cookie 'foo=bar; baz=qux' http://example.com").cookies == {"foo": "bar", "baz": "qux"}


def test_for_multiple_cookies():
    assert parse("curl --cookie 'foo=bar; baz=qux' --cookie 'hello=world' http://example.com").cookies == {
        "foo": "bar", "baz": "qux", "hello": "world"}


def test_for_referer():
    assert parse("curl --referer http://example.com http://example.com").headers['Referer'] == "http://example.com"


def test_for_timeout():
    assert parse("curl --connect-timeout 5 http://example.com").connect_timeout == 5


def test_for_timeout_more_than_times():
    assert parse("curl  --connect-timeout 5 --connect-timeout 10 http://example.com").connect_timeout == 10


def test_for_head():
    assert parse("curl --head http://example.com").request == "HEAD".lower()


def test_for_insecure_false():
    assert parse("curl  http://example.com").insecure == True


def test_for_insecure_true():
    assert parse("curl --insecure http://example.com").insecure is False


def test_for_user_flag():
    assert 'Basic' in parse("curl --user user:pass http://example.com").headers['Authorization']


def test_for_multidata():
    assert parse('curl -d "name=curl" -d "tool=cmdline" https://example.com').data == {
        "name": "curl", "tool": "cmdline"}


def test_for_data_with_and():
    cmd = 'curl --data "name=curl&tool=cmdline" --data version=8.7 https://example.com'
    assert parse(cmd).data == {'name': 'curl', 'tool': 'cmdline','version': '8.7',}


def test_for_json_data():
    cmd = "curl -H 'Content-Type: application/json' -d '{\"foo\": \"bar\"}' http://example.com"
    assert parse(cmd).data == { 'foo': 'bar'}
    assert parse(cmd).headers['Content-Type'] == 'application/json'



def test_for_jsonfy():
    import json
    result  = json.loads(parse("curl  http://example.com",jsonify=True))

    assert isinstance(result,dict)
