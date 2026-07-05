(function() {
  "use strict";

  // Mobile navigation menu toggle
  var navToggle = document.querySelector(".nav-toggle");
  var siteMenu = document.getElementById("site-menu");
  if (navToggle && siteMenu) {
    navToggle.addEventListener("click", function() {
      var isOpen = document.body.classList.toggle("nav-open");
      navToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    });
    siteMenu.addEventListener("click", function(e) {
      if (e.target.closest("a")) {
        document.body.classList.remove("nav-open");
        navToggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  // Header scroll shadow effect
  var siteHeader = document.querySelector(".site-header");
  if (siteHeader) {
    var checkScroll = function() {
      if (window.pageYOffset > 8) {
        siteHeader.classList.add("scrolled");
      } else {
        siteHeader.classList.remove("scrolled");
      }
    };
    checkScroll();
    window.addEventListener("scroll", checkScroll, { passive: true });
  }

  // FAQ accordion toggle
  var faqQuestions = document.querySelectorAll(".faq-q");
  faqQuestions.forEach(function(btn) {
    btn.addEventListener("click", function() {
      var isExpanded = btn.getAttribute("aria-expanded") === "true";
      var contentPanel = document.getElementById(btn.getAttribute("aria-controls"));
      btn.setAttribute("aria-expanded", isExpanded ? "false" : "true");
      if (contentPanel) {
        contentPanel.style.maxHeight = isExpanded ? null : contentPanel.scrollHeight + "px";
      }
    });
  });

  // Reveal animations on scroll (IntersectionObserver)
  var reveals = document.querySelectorAll(".reveal");
  if (reveals.length && "IntersectionObserver" in window) {
    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    reveals.forEach(function(el) {
      observer.observe(el);
    });
  } else {
    reveals.forEach(function(el) {
      el.classList.add("is-visible");
    });
  }

  // Dynamic copyright year updating
  var yrElement = document.getElementById("yr");
  if (yrElement) {
    yrElement.textContent = (new Date()).getFullYear();
  }

  // Homepage Slideshow logic
  var slideshows = document.querySelectorAll(".slideshow-container");
  slideshows.forEach(function(container) {
    var slides = container.querySelectorAll(".slide");
    var dots = container.querySelectorAll(".dot");
    var prevBtn = container.querySelector(".slideshow-prev");
    var nextBtn = container.querySelector(".slideshow-next");
    var currentIndex = 0;
    var timer = null;
    var intervalTime = 5000; // 5 seconds per slide

    function showSlide(index) {
      if (index < 0) {
        index = slides.length - 1;
      } else if (index >= slides.length) {
        index = 0;
      }
      
      slides.forEach(function(slide, i) {
        if (i === index) {
          slide.classList.add("active");
          // Play video if it's a video slide, pause other videos
          var video = slide.querySelector("video");
          if (video) {
            // Avoid calling play() programmatically on initial load (when currentIndex equals index)
            // to allow native HTML autoplay to execute without browser security interruption
            if (currentIndex !== index) {
              video.currentTime = 0;
              video.play().catch(function(err) {
                console.log("Video auto-play blocked: ", err);
              });
            }
          }
        } else {
          slide.classList.remove("active");
          var video = slide.querySelector("video");
          if (video) {
            video.pause();
          }
        }
      });

      dots.forEach(function(dot, i) {
        if (i === index) {
          dot.classList.add("active");
        } else {
          dot.classList.remove("active");
        }
      });

      currentIndex = index;
    }

    function nextSlide() {
      showSlide(currentIndex + 1);
    }

    function prevSlide() {
      showSlide(currentIndex - 1);
    }

    function startTimer() {
      stopTimer();
      timer = setInterval(nextSlide, intervalTime);
    }

    function stopTimer() {
      if (timer) {
        clearInterval(timer);
      }
    }

    if (prevBtn) {
      prevBtn.addEventListener("click", function() {
        prevSlide();
        startTimer();
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener("click", function() {
        nextSlide();
        startTimer();
      });
    }

    dots.forEach(function(dot) {
      dot.addEventListener("click", function() {
        var index = parseInt(dot.getAttribute("data-slide"), 10);
        showSlide(index);
        startTimer();
      });
    });

    // Initialize the first slide and start auto-advance
    showSlide(0);
    startTimer();

    // Pause timer on hover to let users inspect images
    container.addEventListener("mouseenter", stopTimer);
    container.addEventListener("mouseleave", startTimer);
  });
})();