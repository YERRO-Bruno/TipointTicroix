if ('serviceWorker' in navigator) {
  window.addEventListener('load', function() {
      navigator.serviceWorker.register(serviceworker)
          .then(function(registration) {
              console.log('Service Worker enregistré avec succès :', registration.scope);
              alert('Service Worker enregistré avec succès :', registration.scope);
          })
          .catch(function(error) {
              console.log('Échec de l\'enregistrement du Service Worker :', error);
              alert('Échec de l\'enregistrement du Service Worker :', error);
          });
  });
}