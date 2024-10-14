if ('serviceWorker' in navigator) {
  window.addEventListener('load', function() {
      navigator.serviceWorker.register("{% static 'js/service-worker.js' %}")
          .then(function(registration) {
              console.log('Service Worker enregistré avec succès :', registration.scope);
          })
          .catch(function(error) {
              console.log('Échec de l\'enregistrement du Service Worker :', error);
          });
  });
}