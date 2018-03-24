jQuery(function ($) {
    $("#rss-feeds")
        .rss("http://www.betters.stronazen.pl/en/?feed=rss2", {
            limit: 2,
            entryTemplate: '<div class="article-box"><article><h1>{title}</h1><p>{bodyPlain}</p><a href="{url}" target="_blank" class="button-yellow button-small">Read more</a></article><div class="article-image" style="background-image:url({teaserImageUrl})"></div></div>',
        });
    $("#content-slider")
        .rss("http://www.betters.stronazen.pl/en/?feed=rss2", {
            limit: 3,
            entryTemplate: '<div class="slide slide{index}"><div class="slide-content"><a href="{url}" target="_blank">{title}</a></div></div>',
        })
});

// https://github.com/sdepold/jquery-rss/tree/master/examples
// add images to feeds (via plugin):
// https://woorkup.com/show-featured-image-wordpress-rss-feed/#Option-2-8211-Free-Plugin

        