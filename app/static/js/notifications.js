function showItemNotification(itemName, itemDescription) {
    const notification = document.getElementById('itemNotification');
    const nameElement = document.getElementById('itemName');
    const descriptionElement = document.getElementById('itemDescription');
    const acceptButton = document.getElementById('acceptButton');
    const inventoryButton = document.getElementById('inventoryButton');

    nameElement.textContent = itemName;
    descriptionElement.textContent = itemDescription;

    notification.style.opacity = '0';
    notification.style.display = 'block';

    let opacity = 0;
    const fadeIn = setInterval(() => {
        if (opacity >= 1) {
            clearInterval(fadeIn);
        }
        notification.style.opacity = opacity;
        opacity += 0.1;
    }, 50);

    acceptButton.onclick = hideNotification;
    inventoryButton.onclick = () => {
        hideNotification();
        // Добавьте здесь код для перехода в инвентарь
        // Например: window.location.href = '/inventory';
    };

    function hideNotification() {
        let opacity = 1;
        const fadeOut = setInterval(() => {
            if (opacity <= 0) {
                clearInterval(fadeOut);
                notification.style.display = 'none';
            }
            notification.style.opacity = opacity;
            opacity -= 0.1;
        }, 50);
    }
}

$(document).ready(function() {
    $.ajax({
        type: 'GET',
        url: '/get_unread_notifications',
        success: function(notifications) {
            if (notifications.length > 0) {
                showItemNotification(notifications[0].name, notifications[0].description);
            }
        }
    });
});