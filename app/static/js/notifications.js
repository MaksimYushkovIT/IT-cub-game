// Глобальная переменная для хранения ID текущего пользователя
let currentUserId;

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

    fadeElement(notification, 0, 1);

    acceptButton.onclick = hideNotification;
    inventoryButton.onclick = () => {
        hideNotification();
        if (currentUserId) {
            window.location.href = `/profile/${currentUserId}`;
        } else {
            console.error('User ID is not set');
        }
    };

    function hideNotification() {
        fadeElement(notification, 1, 0, () => {
            notification.style.display = 'none';
        });
    }
}

function fadeElement(element, start, end, callback) {
    let opacity = start;
    const step = 0.1;
    const interval = setInterval(() => {
        if ((start < end && opacity >= end) || (start > end && opacity <= end)) {
            clearInterval(interval);
            if (callback) callback();
        }
        element.style.opacity = opacity;
        opacity += (end - start > 0 ? step : -step);
    }, 50);
}


// Функция для установки ID текущего пользователя
function setCurrentUserId(userId) {
    currentUserId = userId;
}

// Вызываем функцию проверки при загрузке страницы
document.addEventListener('DOMContentLoaded', checkUnreadNotifications);

function fadeElement(element, start, end, callback) {
    let opacity = start;
    const step = 0.1;
    const interval = setInterval(() => {
        if ((start < end && opacity >= end) || (start > end && opacity <= end)) {
            clearInterval(interval);
            if (callback) callback();
        }
        element.style.opacity = opacity;
        opacity += (end - start > 0 ? step : -step);
    }, 50);
}

// Функция для проверки непрочитанных уведомлений при загрузке страницы
function checkUnreadNotifications() {
    fetch('/get_unread_notifications')
        .then(response => response.json())
        .then(notifications => {
            notifications.forEach(notification => {
                showItemNotification(notification.name, notification.description);
            });
        })
        .catch(error => console.error('Error:', error));
}

// Вызываем функцию проверки при загрузке страницы
document.addEventListener('DOMContentLoaded', checkUnreadNotifications);

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

function addItemToUser(itemId, quantity = 1) {
    fetch('/add_item_to_user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            item_id: itemId,
            quantity: quantity
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showItemNotification(data.item_name, data.item_description);
        } else {
            console. error('Error:', data.message);
        }
    })
    .catch(error => console.error('Error:', error));
}