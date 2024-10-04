document.addEventListener('DOMContentLoaded', function() {
    const notifications = document.querySelectorAll('.alert');
    notifications.forEach(notification => {
        setTimeout(() => {
            notification.style.opacity = '0';
            notification.style.transform = 'translateY(-20px)';
        }, 3000); // 3 seconds before fading out
    });
});
