function Carousel(settings){
  'use strict';
  settings = settings || {};
  this.carousel = document.querySelector(settings.carousel || '.carousel');
  this.slides = this.carousel.querySelectorAll('ul li');
  this.delay = settings.delay || 10;
  this.autoplay = settings.autoplay === undefined ? true : settings.autoplay;

  this.slides_total = this.slides.length;
  this.current_slide = -1;

  if (this.autoplay) {
    this.play();
  }
}

Carousel.prototype.next = function () {
  'use strict';
  for (var s = 0; s < this.slides.length; s += 1) {
    this.slides[s].style.display = 'none';
 }
  this.current_slide = (this.current_slide + 1) % this.slides.length;
  this.slides[this.current_slide].style.display = 'block';
  this.updateStyleSelected(this.current_slide);

};

Carousel.prototype.prev = function () {
  'use strict';
  for (var s = 0; s < this.slides.length; s += 1) {
    this.slides[s].style.display = 'none';
  }
  this.current_slide = Math.abs(this.current_slide - 1) % this.slides.length;
  this.slides[this.current_slide].style.display = 'block';
   this.updateStyleSelected(this.current_slide);

};
Carousel.prototype.goToSlide = function (num) {
  'use strict'; 
  for (var s = 0; s < this.slides.length; s += 1) {
    this.slides[s].style.display = 'none';
  }
    this.slides[num].style.display = 'block';
    this.updateStyleSelected(num);

};

Carousel.prototype.updateStyleSelected= function (num) {
   for (var s = 0; s < this.slides.length; s += 1) {
  	document.getElementById("carouselnumber"+s).style.background = 'transparent';
  }
   document.getElementById("carouselnumber"+num).style.background = '#eee';
};




Carousel.prototype.play = function () {
  'use strict';
  this.next();
  var that = this;
  if (this.autoplay) {
    this.interval = setTimeout(function () {
      that.play();
    }, this.delay * 1000);
  }
};

Carousel.prototype.stop = function () {
  'use strict';
  if (this.interval) {
    clearInterval(this.interval);
  }
};

