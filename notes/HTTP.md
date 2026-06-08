#HTTP
<!-- GFM-TOC -->
* [HTTP](#http)
    * [1. Basic concepts](#一-Basic concepts)
        * [Request and Response Message](#Request and Response Message)
        * [URL](#url)
    * [2. HTTP method](#二http-method)
        * [GET](#get)
        * [HEAD](#head)
        * [POST](#post)
        * [PUT](#put)
        * [PATCH](#patch)
        * [DELETE](#delete)
        * [OPTIONS](#options)
        * [CONNECT](#connect)
        * [TRACE](#trace)
    * [三、HTTP status code](#三http-STATUSCODE)
        * [1XX information](#1xx-information)
        * [2XX Success](#2xx-Success)
        * [3XX redirect](#3xx-redirect)
        * [4XX Client Error](#4xx-Client Error)
        * [5XX Server Error](#5xx-Server Error)
    * [4. HTTP header](#四http-header)
        * [Universal header field](#general header field)
        * [Request header field](#Request header field)
        * [Response header field](#response header field)
        * [Entity header field](#entity header field)
    * [5. Specific applications](#五specific applications)
        * [Connection Management](#Connection Management)
        * [Cookie](#cookie)
        * [cache](#cache)
        * [Content Negotiation](#contentnegotiation)
        * [Content encoding](#content encoding)
        * [Range Request](#RangeRequest)
        * [chunked transfer encoding](#chunked transfer encoding)
        * [Multi-Part Object Collection](#Multi-Part Object Collection)
        * [Virtual Host](#Virtual Host)
        * [Communication data forwarding](#communication data forwarding)
    * [六、HTTPS](#六https)
        * [Encryption](#encryption)
        *[Certification](#certification)
        * [Integrity Protection](#integrityprotection)
        * [Disadvantages of HTTPS](disadvantages of #https-)
    * [七、HTTP/2.0](#七http20)
        * [HTTP/1.x bug](#http1x-bug)
        * [Binary Framing Layer](#binary framing layer)
        * [Server push](#server push)
        * [Header compression](#Header compression)
    * [Eight, HTTP/1.1 new features](#八http11-new features)
    * [Nine, GET and POST comparison] (#九get-和-post-Comparison)
        * [Function](#Function)
        * [parameter](#parameter)
        * [Security](#security)
        * [Impotence](#Impotence)
        * [cacheable](#cacheable)
        * [XMLHttpRequest](#xmlhttprequest)
    * [References](#references)
<!-- GFM-TOC -->


## 1. Basic concepts

### Request and response messages

The client sends a request message to the server. The server processes the information in the request message and puts the processing result in a response message and returns it to the client.

Request message structure:

- The first line contains the request method, URL, and protocol version;
- The next several lines are request headers. Each header has a header name and a corresponding value.
- A blank line is used to separate the header and content body Body
- Finally the content body of the request

```
GET http://www.example.com/ HTTP/1.1
Accept: text/html,application/xhtml
+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
Cache-Control: max-age=0
Host: www.example.com
If-Modified-Since: Thu, 17 Oct 2019 07:18:26 GMT
If-None-Match: "3147526947+gzip"
Proxy-Connection: keep-alive
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 xxx

param1=1&param2=2
```

Response message structure:

- The first line contains the protocol version, status code and description. The most common one is 200 OK, which means the request was successful.
- The following lines are also the first content
- A blank line separates the header and content body
- Finally, the content body of the response

```
HTTP/1.1 200 OK
Age: 529651
Cache-Control: max-age=604800
Connection: keep-alive
Content-Encoding: gzip
Content-Length: 648
Content-Type: text/html; charset=UTF-8
Date: Mon, 02 Nov 2020 17:53:39 GMT
Etag: "3147526947+ident+gzip"
Expires: Mon, 09 Nov 2020 17:53:39 GMT
Keep-Alive: timeout=4
Last-Modified: Thu, 17 Oct 2019 07:18:26 GMT
Proxy-Connection: keep-alive
Server: ECS (sjc/16DF)
Vary: Accept-Encoding
X-Cache: HIT

<!doctype html>
<html>
<head>
    <title>Example Domain</title>
	// Omit...
</body>
</html>

```

### URL

HTTP uses URL (**U** niform **R**esource **L**ocator, Uniform Resource Locator) to locate resources, which is a subset of URI (**U**niform **R**esource **I**dentifier, Uniform Resource Identifier). URL adds positioning capabilities based on URI. In addition to the URL, the URI also contains the URN (Uniform Reso
urce Name (Uniform Resource Name), which is only used to define the name of a resource and does not have the ability to locate the resource. For example, urn:isbn:0451450523 is used to define a book name, but it does not indicate how to find the book.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/8441b2c4-dca7-4d6b-8efb-f22efccaf331.png" width="500px"> </div><br>

- [wikipedia: Uniform Resource Identifier](https://zh.wikipedia.org/wiki/Uniform Resource Identifier)
- [wikipedia: URL](https://en.wikipedia.org/wiki/URL)
- [rfc2616:3.2.2 http URL](https://www.w3.org/Protocols/rfc2616/rfc2616-sec3.html#sec3.2.2)
- [What is the difference between a URI, a URL and a URN?](https://stackoverflow.com/questions/176264/what-is-the-difference-between-a-uri-a-url-and-a-urn)

## 2. HTTP method

The first line of the **request message** sent by the client is the request line, which contains the method field.

###GET

> Get resources

Most of the current network requests use the GET method.

### HEAD

> Get the message header

Similar to the GET method, but does not return the body part of the message entity.

Mainly used to confirm the validity of the URL and the date and time of resource updates.

### POST

>Transfer entity body

POST is mainly used to transmit data, while GET is mainly used to obtain resources.

See Chapter 9 for more comparisons of POST and GET.

##
# PUT

> Upload files

Since it does not have a verification mechanism, anyone can upload files, so there are security issues and this method is generally not used.

```html
PUT /new.html HTTP/1.1
Host: example.com
Content-type: text/html
Content-length: 16

<p>New File</p>
```

### PATCH

> Make partial modifications to resources

PUT can also be used to modify resources, but it can only completely replace the original resource, while PATCH allows partial modification.

```html
PATCH /file.txt HTTP/1.1
Host: www.example.com
Content-Type: application/example
If-Match: "e0023aa4e"
Content-Length: 100

[description of changes]
```

### DELETE

> Delete files

The opposite function of PUT and also without verification mechanism.

```html
DELETE /file.html HTTP/1.1
```

### OPTIONS

> Query supported methods

Query the methods supported by the specified URL.

Will return something like `Allow: GET, POST, HEAD, OPTIONS`.

### CONNECT

> Require tunneling when communicating with proxy server

Use SSL (Secure Sockets Layer, Secure Sockets Layer) and TLS (Transport Layer Security, Transport Layer Security) protocols to encrypt the communication content and then transmit it through the network tunnel.

```html
CONNECT www.example.com:443 HTTP/1.1
```

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/dc00f70e-c5c8-4d20-baf1-2d70014a97e3.jpg" width=""/> </div><br>

### TRACE

> Trace the path

The server returns the communication path to the client.

When sending a request, fill in the value in the Max-Forwards header field. Each time it passes through a server, it will be subtracted by 1. When the value is 0, the transmission will stop.

TRACE is generally not used and is vulnerable to XST attacks (Cross-Site Tracing).

- [rfc2616:9 Method Definitions](https://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html)

## 3. HTTP status code

The first line in the **response message** returned by the server is the status line, which contains the status code and reason phrase to inform the client of the result of the request.

| Status Code | Category | Meaning |
| :---: | :---: | :---: |
| 1XX | Informational (informational status code) | The received request is being processed |
| 2XX | Success (success status code) | The request is processed normally |
| 3XX | Redirection (redirect status code) | Additional action is required to complete the request |
| 4XX | Client Error (client error status code) | The server cannot process the request |
| 5XX | Server Error (server error status code) | Server error in processing the request |

### 1XX Information

- **100 Continue**: Indicates that everything is normal so far and the client can continue to send requests or ignore this response.

### 2XX Success

- **200 OK**

- **204 No Content**: The request has been successfully processed, but the response message returned does not contain the body part of the entity. Generally used when you only need to send information from the client
to the server without returning data.

- **206 Partial Content**: Indicates that the client made a range request, and the response message contains the entity content in the range specified by Content-Range.

### 3XX redirect

- **301 Moved Permanently** : Permanent redirection

- **302 Found**: Temporary redirection

- **303 See Other**: has the same function as 302, but 303 explicitly requires that the client should use the GET method to obtain resources.

- Note: Although the HTTP protocol stipulates that changing the POST method to the GET method is not allowed when redirecting in the 301, 302 status, most browsers will change the POST method to the GET method in the redirection of the 301, 302, and 303 status.

- **304 Not Modified**: If the request message header contains some conditions, such as: If-Match, If-Modified-Since, If-None-Match, If-Range, If-Unmodified-Since, if the conditions are not met, the server will return
304 status code.

- **307 Temporary Redirect**: Temporary redirect, similar in meaning to 302, but 307 requires the browser not to change the POST method of the redirect request to the GET method.

### 4XX client error

- **400 Bad Request**: There is a syntax error in the request message.

- **401 Unauthorized**: This status code indicates that the request sent requires authentication information (BASIC authentication, DIGEST authentication). If a request has been made before, user authentication failed.

- **403 Forbidden**: The request was rejected.

- **404 Not Found**

### 5XX server error

- **500 Internal Server Error**: An error occurred while the server was executing the request.

- **503 Service Unavailable**: The server is temporarily overloaded or is undergoing downtime for maintenance, and is now unable to process requests.

## 4. HTTP header

There are 4 types of header fields: general header fields, request header fields, response header fields and entity header fields.

The various header fields and their meanings are as follows (no need to remember them all, just for reference):

### Common header fields

| Header field name | Description |
| :--: | :--: |
| Cache-Control | Control cache behavior |
| Connection | Control header fields that are no longer forwarded to the proxy, manage persistent connections |
| Date | The date and time when the message was created |
| Pragma | Message command |
| Trailer | List of headers at the end of the message |
| Transfer-Encoding | Specify the transfer encoding method of the message body |
| Upgrade | Upgrade to other protocols |
| Via | Information about proxy servers |
| Warning | Error notification |

### Request header fields

| Header field name | Description |
| :--: | :--: |
| Accept | Media types that the user agent can handle |
| Accept-Charset | Preferred character set |
| Accept-Encoding | Preferred content encoding |
| Accept-Language | Preferred language (natural language) |
| Authorization | Web authentication information |
| Expect | Expect specific b
ehavior from the server |
| From | User's email address |
| Host | The server where the requested resource is located |
| If-Match | Compare Entity Tags (ETag) |
| If-Modified-Since | Compare the update time of resources |
| If-None-Match | Compares entity tags (opposite of If-Match) |
| If-Range | Send a range request for entity Byte when the resource is not updated |
| If-Unmodified-Since | Compares the update time of a resource (opposite of If-Modified-Since) |
| Max-Forwards | Maximum number of transmission hops |
| Proxy-Authorization | The proxy server requires the client's authentication information |
| Range | Byte range request for the entity |
| Referer | The original getter of the URI in the request |
| TE | Transfer encoding priority |
| User-Agent | HTTP client program information |

### Response header fields

| Header field name | Description |
| :--: | :--: |
| Accept-Ranges | Whether to accept byte range requests |
| Age | Elapsed time of estimated resource creation |
| ETag | Resource matching information |
| Location | Redirects the client to the specified URI |
| Proxy-Authenticate | Authentication information of the proxy server to the client |
| Retry-After | Timing requirements for reinitiating requests |
| Server | HTTP server installation information |
| Vary | Management information cached by the proxy server |
| WWW-Authenticate | Server-to-client authentication information |

### Entity header field

| Header field name | Description |
| :--: | :--: |
| Allow | HTTP methods supported by the resource |
| Content-Encoding | The encoding method applicable to the entity body |
| Content-Language | The natural language of the entity subject |
| Content-Length | The size of the entity body |
| Content-Location | Replaces the URI of the corresponding resource |
| Content-MD5 | Message digest of the entity subject |
| Content-Range | The location range of the entity body |
| Content-Type | The media type of the entity body |
| Expires | The date and time when the entity body expires |
| Last-Modified | The last modified date and time of the resource |

## 5. Specific applications

### Connection management

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/HTTP1_x_Connections.png" width="800"/> </div><br>

#### 1. Short connection and long connection

When the browser accesses an HTML page that contains multiple images, in addition to requesting the accessed HTML page resources, it will also request image resources. If a new TCP connection is required for each HTTP communication, the overhead will be very high.

A long connection only needs to establish a TCP connection once to carry out multiple HTTP communications.

- Starting from HTTP/1.1, the default is long connection. If you want to disconnect, you need to initiate the disconnection from the client or server, use `Connection: close`;
- Before HTTP/1.1, the default was short connection. If you need to use long connection, use `Conne
ction: Keep-Alive`.

#### 2. Assembly line

By default, HTTP requests are issued sequentially, and the next request is not issued until a response is received for the current request. Due to network latency and bandwidth limitations, it may take a long time before the next request is sent to the server.

Pipelining is to continuously issue requests on the same long connection without waiting for a response to return, which can reduce latency.

### Cookies

The HTTP protocol is stateless, mainly to make the HTTP protocol as simple as possible so that it can handle a large number of transactions. HTTP/1.1 introduced cookies to save state information.

A cookie is a small piece of data sent by the server to the user's browser and saved locally. It will be carried when the browser makes another request to the same server to inform the server whether the two requests come from the same browser. Since each subsequent request will need to carry cookie data, it will bring additional performance overhead (especially in a mobile environment).

Cookies were once used to store client data as the only storage method because there was no other suitable storage method at that time. However, as modern browsers begin to support various storage methods, Cookies are gradually being eliminated. New browser APIs already allow developers to store data directly locally, such as using Web storage
e API (local storage and session storage) or IndexedDB.

#### 1. Purpose

- Session state management (such as user login status, shopping cart, game scores or other information that needs to be recorded)
- Personalized settings (such as user-defined settings, themes, etc.)
- Browser behavior tracking (such as tracking and analyzing user behavior, etc.)

#### 2. Creation process

The response message sent by the server contains the Set-Cookie header field. After receiving the response message, the client saves the Cookie content to the browser.

```html
HTTP/1.0 200 OK
Content-type: text/html
Set-Cookie: yummy_cookie=choco
Set-Cookie: tasty_cookie=strawberry

[page content]
```

When the client subsequently sends a request to the same server, the cookie information will be retrieved from the browser and sent to the server through the Cookie request header field.

```html
GET /sample_page.html HTTP/1.1
Host: www.example.org
Cookie: yummy_cookie=choco; tasty_cookie=strawberry
```

#### 3. Classification

- Session Cookie: It is automatically deleted after the browser is closed, which means it is only valid during the session.
- Persistent Cookie: After specifying the expiration time (Expires) or validity period (max-age), it becomes a persistent Cookie.

```html
Set-Cookie: id=a3fWa; Expires=Wed, 21 Oct 2015 07:28:00 GMT;
```

#### 4. Scope

The Domain ID specifies which hosts can accept cookies. If not specified, it defaults to the host of the current document (excluding subdomain names). If Domain is specified, subdomain names are generally included. For example, if you set Doma
in=mozilla.org, the cookie is also included in the subdomain (such as developer.mozilla.org).

The Path identifier specifies which paths under the host can accept cookies (the URL path must exist in the request URL). Subpaths are also matched using the character %x2F ("/") as a path separator. For example, if you set Path=/docs, the following addresses will match:

-/docs
- /docs/Web/
- /docs/Web/HTTP

#### 5. JavaScript

The browser can create new cookies through the `document.cookie` property, and can also access non-HttpOnly tagged cookies through this property.

```html
document.cookie = "yummy_cookie=choco";
document.cookie = "tasty_cookie=strawberry";
console.log(document.cookie);
```

#### 6. HttpOnly

Cookies marked HttpOnly cannot be called by JavaScript scripts. Cross-site scripting attacks (XSS) often use JavaScript's `document.cookie` API to steal users' cookie information, so using the HttpOnly tag can avoid XSS attacks to a certain extent.

```html
Set-Cookie: id=a3fWa; Expires=Wed, 21 Oct 2015 07:28:00 GMT; Secure; HttpOnly
```

#### 7. Secure

Cookies marked Secure can only be sent to the server through requests encrypted by the HTTPS protocol. But even if the Secure flag is set, sensitive information should not be transmitted through cookies, because cookies are inherently insecure, and the Secure flag cannot provide reliable security.

#### 8. Session

In addition to storing user information in the user's browser through cookies, you can also use Session to store it on the server side. Information stored on the server side is more secure.

Sessions can be stored in files, databases, or in memory on the server. Session can also be stored in an in-memory database such as Redis, which will be more efficient.

The process of using Session to maintain user login status is as follows:

- When the user logs in, the user submits a form containing the user name and password and puts it in the HTTP request message;
- The server verifies the username and password, and if correct, stores the user information in Redis. Its Key in Redis is called Session ID;
- The Set-Cookie header field of the response message returned by the server contains the Session ID. After receiving the response message, the client stores the Cookie value in the browser;
- The client will include the cookie value when making subsequent requests to the same server. After receiving it, the server will extract the Session ID, retrieve the user information from Redis, and continue the previous business operations.

Attention should be paid to the security issue of Session ID. It cannot be easily obtained by malicious attackers, so it cannot generate a Session ID value that can be easily guessed. Additionally, Session IDs need to be regenerated frequently. In scenarios with extremely high security requirements, such as transfers and other operations, in addition to using Session to manage user status, users also need to be re-verified, such as re-entering passwords or usin
g SMS verification codes.

#### 9. Disable Cookies in the browser

At this time, Cookie cannot be used to save user information, only Session can be used. In addition, the Session ID can no longer be stored in Cookie. Instead, URL rewriting technology is used to pass the Session ID as a parameter of the URL.

#### 10. Cookie and Session selection

- Cookies can only store ASCII code strings, while Sessions can store any type of data, so Sessions are preferred when considering data complexity;
- Cookies are stored in the browser and are susceptible to malicious viewing. If you must store some private data in a cookie, you can encrypt the cookie value and then decrypt it on the server;
- For large websites, if all user information is stored in Session, the overhead will be very large, so it is not recommended to store all user information in Session.

### Cache

#### 1. Advantages

- Relieve server pressure;
- Reduce the latency for the client to obtain resources: the cache is usually located in memory and reads from the cache are faster. And the cache server may also be geographically closer to the origin server, such as browser cache.

#### 2. Implementation method

- Let the proxy server cache;
- Let the client browser do the caching.

#### 3. Cache-Control

HTTP/1.1 controls caching through the Cache-Control header field.

**3.1 Disable caching**

The no-store directive specifies that no part of the request or response should be cached.

```html
Cache-Control: no-store
```

**3.2 Forced confirmation caching**

The no-cache directive stipulates that the cache server needs to first verify the validity of the cache resource with the origin server. Only
Only when the cached resource is valid can the cache be used to respond to the client's request.

```html
Cache-Control: no-cache
```

**3.3 Private cache and public cache**

The private directive stipulates that the resource is used as a private cache, which can only be used by a single user, and is generally stored in the user's browser.

```html
Cache-Control: private
```

The public directive stipulates that the resource should be used as a public cache, which can be used by multiple users and is generally stored in a proxy server.

```html
Cache-Control: public
```

**3.4 Cache expiration mechanism**

The max-age directive appears in the request message, and the cache time of the cached resource is less than the time specified by the directive, then the cache can be accepted.

The max-age directive appears in the response message and indicates the time the cache resource is stored in the cache server.

```html
Cache-Control: max-age=31536000
```

The Expires header field can also be used to tell the cache server when the resource will expire.

```html
Expires: Wed, 04 Jul 2012 08:26:05 GMT
```

- In HTTP/1.1, the max-age directive will be processed first;
- In HTTP/1.0, the max-age directive is ignored.

#### 4. Cache verification

You need to first understand the meaning of the ETag header fie
ld, which is the unique identifier of the resource. URL cannot uniquely represent resources. For example, `http://www.google.com/` has two resources, Chinese and English. Only ETag can uniquely identify these two resources.

```html
ETag: "82e22293907ce725faf67773957acd12"
```

You can put the ETag value of the cached resource into the If-None-Match header. After receiving the request, the server determines whether the ETag value of the cached resource is consistent with the latest ETag value of the resource. If they are consistent, it means that the cached resource is valid and returns 304 Not Modified.

```html
If-None-Match: "82e22293907ce725faf67773957acd12"
```

The Last-Modified header field can also be used for cache verification. It is included in the response message sent by the origin server and indicates the last modification time of the resource by the origin server. However, it is a weak validator because it is only accurate to one second, so it is usually used as a fallback for ETags. If the response header field contains this information, the client can include If-Modified-Since in subsequent requests to verify the cache. The server will only return the resource with a status code of 200 OK if the content of the requested resource has been modified since the given date and time. If the requested resource has not been modified since then, a 304 Not Modified response message without an entity body is returned.

```html
Last-Modified: Wed, 21 Oct 2015 07:28:00 GMT
```

```html
If-Modified-Since: Wed, 21 Oct 2015 07:28:00 GMT
```

### Content Negotiation

Return the most appropriate content through content negotiation, such as returning a Chinese interface or an English interface according to the browser's default language.

#### 1. Type

**1.1 Server-driven**

The client sets specific HTTP header fields, such as Accept, Accept-Charset, Accept-Encoding, and Accept-Language, and the server returns specific resources based on these fields.

It has the following problems:

- It is difficult for the server to know all the information about the client browser;
- The information provided by the client is quite verbose (the header compression mechanism of the HTTP/2 protocol alleviates this problem), and there are privacy risks (HTTP fingerprinting technology);
- A given resource needs to return different presentation forms, the efficiency of the shared cache will be reduced, and the server-side implementation will become more and more complex.

**1.2 Agent driven**

The server returns 300 Multiple Choices or 406 Not Acceptable, and the client selects the most appropriate resource.

#### 2. Vary

```html
Vary: Accept-Language
```

In the case of using content negotiation, the cache in the cache server can only be used if it meets the content negotiation conditions, otherwise the resource should be requested from the origin server.

For example, after a client sends a request containing the Accept-Language header field, the response returned b
y the origin server contains the content of `Vary: Accept-Language`. After the cache server caches the response, the cache will be returned only when the client accesses the same URL resource next time and Accept-Language is the same as the corresponding value in the cache.

### Content encoding

Content encoding compresses the entity body, thereby reducing the amount of data transmitted.

Commonly used content encodings include: gzip, compress, deflate, and identity.

The browser sends the Accept-Encoding header, which contains the compression algorithms it supports and their respective priorities. The server chooses one of them, uses that algorithm to compress the response message body, and sends a Content-Encoding header to tell the browser which algorithm it has chosen. Since the content negotiation process selects the resource presentation form based on the encoding type, the Vary header field of the response message must at least contain Content-Encoding.

### Range request

If there is a network outage and the server only sends part of the data, a range request allows the client to request only the part of the data that the server did not send, thus preventing the server from resending all the data.

#### 1. Range

Add the Range header field to the request message to specify the requested range.

```html
GET /z4d4kWk.jpg HTTP/1.1
Host: i.imgur.com
Range: bytes=0-1023
```

If the request is successful, the response returned by the server contains the 206 Partial Content status code.

```html
HTTP/1.1 206 Partial Content
Content-Range: bytes 0-1023/146515
Content-Length: 1024
...
(binary content)
```

#### 2. Accept-Ranges

The response header field Accept-Ranges is used to tell the client whether it can handle the range request. Bytes can be used, otherwise none.

```html
Accept-Ranges: bytes
```

#### 3. Response status code

- If the request is successful, the server will return a 206 Partial Content status code.
- In the case where the requested range is out of bounds, the server will return the 416 Requested Range Not Satisfiable status code.
- In cases where range requests are not supported, the server returns a 200 OK status code.

### Chunked transfer encoding

Chunked Transfer Encoding can split data into multiple chunks, allowing the browser to display the page step by step.

###Multipart object collection

A message body can contain multiple types of entities sent at the same time. Each part is separated by the delimiter defined by the boundary field. Each part
All can have header fields.

For example, when uploading multiple forms, you can use the following methods:

```html
Content-Type: multipart/form-data; boundary=AaB03x

--AaB03x
Content-Disposition: form-data; name="submit-name"

Larry
--AaB03x
Content-Disposition: form-data; name="files"; filename="file1.txt"
Content-Type: text/plain

... contents of file1.txt ...
--AaB03x--
```

### Virtual host

HTTP/1.1 uses virtual host technology so that one server has multiple domain
names and can be logically viewed as multiple servers.

### Communication data forwarding

#### 1. Agent

The proxy server accepts the client's request and forwards it to other servers.

The main purposes of using a proxy are:

- cache
- Load balancing
- Network access control
- Access logging

Proxy servers are divided into two types: forward proxy and reverse proxy:

- The user is aware of the existence of the forward proxy.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/a314bb79-5b18-4e63-a976-3448bffa6f1b.png" width=""/> </div><br>

- Reverse proxies are generally located in the internal network and are not visible to users.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/2d09a847-b854-439c-9198-b29c65810944.png" width=""/> </div><br>

#### 2. Gateway

Unlike proxy servers, gateway servers convert HTTP into other protocols for communication, thereby requesting services from other non-HTTP servers.

#### 3. Tunnel

Use encryption such as SSL to establish a secure communication line between the client and server.

## 6. HTTPS

HTTP has the following security issues:

- Use clear text for communication, and the content may be eavesdropped;
- Without verifying the identity of the communicating party, the communicating party's identity may be disguised;
- The integrity of the message cannot be proven, and the message may be tampered with.

HTTPS is not a new protocol. Instead, HTTP communicates with SSL (Secure Sockets Layer) first, and then SSL communicates with TCP. In other words, HTTPS uses a tunnel for communication.

By using SSL, HTTPS has encryption (anti-eavesdropping), authentication (anti-masking), and integrity protection (anti-tampering).

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/ssl-offloading.jpg" width="700"/> </div><br>

### Encryption

#### 1. Symmetric key encryption

Symmetric-Key Encryption uses the same key for encryption and decryption.

- Advantages: fast computing speed;
- Disadvantage: Unable to securely transmit the key to the communicating party.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/7fffa4b8-b36d-471f-ad0c-a88ee763bb76.png" width="600"/> </div><br>

#### 2. Asymmetric key encryption

Asymmetric key encryption, also known as Public-Key Encryption, uses different keys for encryption and decryption.

The public key is available to everyone. After the communication sender obtains the recipient's public key, it can use the public key to encrypt. The recipient uses the private key to decrypt the communication content after receiving it.

In addition to being used for encryption, asymmetric keys can also be used for signing. Because the private key cannot be obtained by others, the sender of the communication uses his private key to sign, and the receiver of the communication uses the sender's public key to decrypt the signature to determine w
hether the signature is correct.

- Advantages: The public key can be transmitted to the communication sender more securely;
- Disadvantages: slow operation speed.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/39ccb299-ee99-4dd1-b8b4-2f9ec9495cb4.png" width="600"/> </div><br>

#### 3. Encryption method used by HTTPS

As mentioned above, the transmission efficiency of symmetric key encryption is higher, but the Secret Key cannot be safely transmitted to the communicating party. Asymmetric key encryption can ensure the security of transmission, so we can use asymmetric key encryption to transmit the Secret Key to the communicating party. HTTPS uses a hybrid encryption mechanism, which takes advantage of the solution mentioned above:

- Use asymmetric key encryption to transmit the Secret Key required for symmetric key encryption to ensure security;
- After obtaining the Secret Key, use symmetric key encryption to communicate to ensure efficiency. (The Session Key in the picture below is the Secret Key)

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/How-HTTPS-Works.png" width="600"/> </div><br>

### Certification

The communicating parties are authenticated by using **certificates**.

Digital Certificate Authority (CA, Certificate Authority) is a third-party organization that is trustworthy for both the client and the server.

The operator of the server applies for a public key to the CA. After the CA determines the identity of the applicant, it will digitally sign the applied public key, then distribute the signed public key, put the public key into the public key certificate and bind it together.

When communicating over HTTPS, the server sends the certificate to the client. After the client obtains the public key, it first uses the digital signature for verification. If the verification passes, communication can begin.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/2017-06-11-ca.png" width=""/> </div><br>

### Integrity protection

SSL provides message digest functionality for integrity protection.

HTTP also provides MD5 message digest function, but it is not secure. For example, after the message content is tampered with, the MD5 value is recalculated at the same time, and the communication receiver cannot realize that the tampering has occurred.

The message digest feature of HTTPS is secure because it combines encryption and authentication. Just imagine, after the encrypted message is tampered with, it is difficult to re-
Calculate the message digest since the plaintext cannot be easily obtained.

### Disadvantages of HTTPS

- Because processes such as encryption and decryption are required, the speed will be slower;
- Need to pay high fees for certificate authorization.

## 7. HTTP/2.0

### HTTP/1.x flaws

HTTP/1.x implementation simplicity comes at the expense of performance:

- The client needs to use multiple c
onnections to achieve concurrency and reduce latency;
- Will not compress request and response headers, causing unnecessary network traffic;
- No support for effective resource prioritization, resulting in poor utilization of underlying TCP connections.

### Binary Framing Layer

HTTP/2.0 divides messages into HEADERS frames and DATA frames, both of which are in binary format.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/86e6a91d-a285-447a-9345-c5484b8d0c47.png" width="400"/> </div><br>

During the communication process, only one TCP connection will exist, which carries any number of bidirectional data streams (Stream).

- A data stream (Stream) has a unique identifier and optional priority information, used to carry bidirectional information.
- A message is a complete series of frames corresponding to a logical request or response.
- Frame is the smallest communication unit. Frames from different data streams can be sent interleaved and then reassembled based on the data stream identifier in each frame header.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/af198da1-2480-4043-b07f-a3b91a88b815.png" width="600"/> </div><br>

### Server push

When the client requests a resource, HTTP/2.0 will send the related resources to the client together, so the client does not need to initiate a request again. For example, when the client requests the page.html page, the server sends script.js, style.css and other related resources to the client.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/e3f1657c-80fc-4dfa-9643-bf51abd201c6.png" width="800"/> </div><br>

### Header compression

The HTTP/1.1 header contains a lot of information and must be sent repeatedly every time.

HTTP/2.0 requires the client and server to simultaneously maintain and update a table of previously seen header fields, thus avoiding repeated transmissions.

Not only that, HTTP/2.0 also uses Huffman encoding to compress header fields.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/_u4E0B_u8F7D.png" width="600"/> </div><br>

## 8. HTTP/1.1 new features

See above for details

- The default is long connection
- Support pipeline
-Supports opening multiple TCP connections at the same time
- Support virtual hosting
- Added status code 100
- Supports chunked transfer encoding
- Added cache processing instruction max-age

## 9. Comparison of GET and POST

### Function

GET is used to obtain resources, while POST is used to transfer the entity body.

### Parameters

Both GET and POST requests can use additional parameters, but GET parameters appear in the URL as query strings, while POST parameters are stored in the entity body. Just because POST parameters are stored in the entity body does not mean it is more secure, because it can still be viewed through some packet capture tools (Fiddler).

Because the URL only supports ASC
II code, if there are Chinese and other characters in the GET parameters, they need to be encoded first. For example, `Chinese` will be converted to `%E4%B8%AD%E6%96%87`, and spaces will be converted to `%20`. POST parameters support standard character sets.

```
GET /test/demo_form.asp?name1=value1&name2=value2 HTTP/1.1
```

```
POST /test/demo_form.asp HTTP/1.1
Host: w3schools.com
name1=value1&name2=value2
```

### Security

Safe HTTP methods do not change server state, which means it is only readable.

The GET method is safe, but POST is not, because the purpose of POST is to transmit the entity body content. This content may be form data uploaded by the user. After the upload is successful, the server may store this data in the database, so the status changes.

In addition to GET, safe methods include: HEAD and OPTIONS.

In addition to POST, unsafe methods include PUT and DELETE.

### Idempotence

For idempotent HTTP methods, the effect of executing the same request once and multiple times in succession is the same, and the status of the server is also the same. In other words, idempotent methods should not have side effects (except for statistical purposes).

All security methods are also idempotent.

Methods such as GET, HEAD, PUT, and DELETE are all idempotent when implemented correctly, while the POST method is not.

GET /pageX HTTP/1.1 is idempotent. If called multiple times in succession, the client will receive the same result:

```
GET /pageX HTTP/1.1
GET /pageX HTTP/1.1
GET /pageX HTTP/1.1
GET /pageX HTTP/1.1
```

POST /add_row HTTP/1.1 is not idempotent. If called multiple times, multiple rows of records will be added:

```
POST /add_row HTTP/1.1 -> Adds a 1nd row
POST /add_row HTTP/1.1 -> Adds a 2nd row
POST /add_row HTTP/1.1 -> Adds a 3rd row
```

DELETE /idX/delete HTTP/1.1 is idempotent, even if different requests receive different status codes:

```
DELETE /idX/delete HTTP/1.1 -> Returns 200 if idX exists
DELETE /idX/delete HTTP/1.1 -> Returns 404 as it just got deleted
DELETE /idX/delete HTTP/1.1 -> Returns 404
```

### Cacheable

If you want to cache the response, the following conditions need to be met:

- The HTTP method of the request message itself is cacheable, including GET and HEAD, but PUT and DELETE are not cacheable, and POST is not cacheable in most cases.
- The status code of the response message is cacheable, including: 200, 203, 204, 206, 300, 301, 404, 405,
410, 414, and 501.
- The Cache-Control header field of the response message does not specify caching.

### XMLHttpRequest

To illustrate another difference between POST and GET, you need to first understand XMLHttpRequest:

> XMLHttpRequest is an API that provides the client with the functionality to transfer data between the client and server. It provides a simple way to get data via a URL without causing the entire page to refresh. This allows the web page to update only part of the page without disturbing the user. XMLHttpRequest is heavily used in AJAX.
- When using the POST method of XMLHttpRequest, the browser will send the Header first and then the Data. But not all browsers will do this, such as Firefox.
- The GET method Header and Data will be sent together.

## References

- Nobu Ueno. Illustration of HTTP[M]. People's Posts and Telecommunications Publishing House, 2014.
- [MDN: HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP)
- [Introduction to HTTP/2](https://developers.google.com/web/fundamentals/performance/http2/?hl=zh-cn)
- [htmlspecialchars](http://php.net/manual/zh/function.htmlspecialchars.php)
- [Difference between file URI and URL in java](http://java2db.com/java-io/how-to-get-and-the-difference-between-file-uri-and-url-in-java)
- [How to Fix SQL Injection Using Java PreparedStatement & CallableStatement](https://software-security.sans.org/developer-how-to/fix-sql-injection-in-java-using-prepared-callable-statement)
- [A brief discussion on the difference between Get and Post in HTTP](https://www.cnblogs.com/hyddd/archive/2009/03/31/1426026.html)
- [Are http:// and www really necessary?](https://www.webdancers.com/are-http-and-www-necesary/)
- [HTTP (HyperText Transfer Protocol)](https://www.ntu.edu.sg/home/ehchua/programming/webprogramming/HTTP_Basics.html)
- [Web-VPN: Secure Proxies with SPDY & Chrome](https://www.igvita.com/2011/12/01/web-vpn-secure-proxies-with-spdy-chrome/)
- [File:HTTP persistent connection.svg](http://en.wikipedia.org/wiki/File:HTTP_persistent_connection.svg)
- [Proxy server](https://en.wikipedia.org/wiki/Proxy_server)
- [What Is This HTTPS/SSL Thing And Why Should You Care?](https://www.x-cart.com/blog/what-is-https-and-ssl.html)
- [What is SSL Offloading?](https://securebox.comodo.com/ssl-sniffing/ssl-offloading/)
- [Sun Directory Server Enterprise Edition 7.0 Reference - Key Encryption](https://docs.oracle.com/cd/E19424-01/820-4811/6ng8i26bn/index.html)
- [An Introduction to Mutual SSL Authentication](https://www.codeproject.com/Articles/326574/An-Introduction-to-Mutual-SSL-Authentication)
- [The Difference Between URLs and URIs](https://danielmiessler.com/study/url-uri/)
- [The difference between Cookie and Session](https://juejin.im/entry/5766c29d6be3ff006a31b84e#comment)
- [What is the difference between COOKIE and SESSION](https://www.zhihu.com/question/19786827)
- [Cookie/Session mechanism and security](https://harttle.land/2015/08/10/cookie-session.html)
- [HTTPS Certificate Principle](https://shijianan.com/2017/06/11/https/)
- [What is the difference between a URI, a URL and a URN?](https://stackoverflow.com/questions/176264/what-is-the-difference-between-a-uri-a-url-and-a-urn)
- [XMLHttpRequest](https://developer.mozilla.org/zh-CN/docs/Web/API/XMLHttpRequest)
- [XMLHttpRequest (XHR) Uses Multiple Packets for HTTP POST?](https://blog.josephscott.org/2009/08/27/xmlhttprequest-xhr-uses-multiple-packets-for-http-post/)
- [Symmetric vs. Asymmetric Encryption – What are differences?](https://www.ssl2buy.com/wiki/symmetric-vs-asymmetric-encry
ption-what-are-differences)
- [Web performance optimization with HTTP/2
](https://www.kancloud.cn/digest/web-performance-http2)
- [Introduction to HTTP/2](https://developers.google.com/web/fundamentals/performance/http2/?hl=zh-cn)
