# TODO
* Allow enabling per server/buffer/nick.
* Can break in long PRIVMSG lines, if translation would make them even
  longer (unlikely). If the resulting line exceeds 512 chars (RFC 2812), god
  knows what happens, I didn't check in weechat.
* Can break in case when source PRIVMSG text does not contain spaces and is not
  prefixed with ' :'. If the resulting text contains spaces (unlikely), it
  won't be prepended with ' :', thus resulting in multiple arguments.
  It would either break the delivery completely or just deliver the first
  argument up to space, I didn't check.
* Reuse the HTML2Text? Is it safe?
* Remove emphasis, not much needed I suppose.
