/*
* Collision Check Plugin v1.1
* Copyright (c) Constantin Groß, 48design.de
* v1.2 rewrite with thanks to Daniel
*
* @requires jQuery v1.3.2
*
* Dual licensed under the MIT and GPL licenses:
*   http://www.opensource.org/licenses/mit-license.php
*   http://www.gnu.org/licenses/gpl.html
*
*/
(function(a){a.fn.collidesWith=function(e){var b=this;var d=a(e);var f=a([]);if(!b||!d){return false}b.each(function(){var i=a(this);var g=i.offset();var h=g.left;var c=g.top;var k=h+i.outerWidth();var j=c+i.outerHeight();d.not(i).each(function(){var o=a(this);var l=o.offset();var q=l.left;var p=l.top;var n=q+o.outerWidth();var m=p+o.outerHeight();if(h>=n||k<=q||c>=m||j<=p){return true}else{if(f.length==f.not(this).length){f.push(this)}}})});return f}})(jQuery);