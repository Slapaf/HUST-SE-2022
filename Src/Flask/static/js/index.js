gsap.registerPlugin(ScrollTrigger);

let panels = gsap.utils.toArray(".panel"),
    scrollTween;

function goToSection(i) {
  scrollTween = gsap.to(window, {
    scrollTo: {y: i * innerHeight, autoKill: false},
    duration: 1,
    onComplete: () => scrollTween = null,
    overwrite: true
  });
}

panels.forEach((panel, i) => {
  ScrollTrigger.create({
    trigger: panel,
    start: "top bottom",
    end: "+=200%",
    onToggle: self => self.isActive && !scrollTween && goToSection(i)
  });
});

// just in case the user forces the scroll to an inbetween spot (like a momentum scroll on a Mac that ends AFTER the scrollTo tween finishes):
ScrollTrigger.create({
  start: top, 
  end: "max",
  snap: 1 / (panels.length - 1)
});


// document.addEventListener('DOMContentLoaded', function () {
//     window.setTimeout(document.querySelector('svg').classList.add('animated'),1000);
// });

