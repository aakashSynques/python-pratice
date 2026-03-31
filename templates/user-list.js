// simple-user-list.js

async function loadUsersList(containerId) {

    try {

        const res = await fetch('/users/all', {
            headers: getAuthHeaders()
        });

        if (!res.ok) {
            throw new Error("Users fetch failed");
        }

        const usersData = await res.json();

        const container = document.getElementById(containerId);

        if (!container) {
            console.warn("Container not found:", containerId);
            return;
        }

        container.innerHTML = "";

        usersData.forEach(user => {

            const item = document.createElement("div");

            item.className = "card mb-2 p-2";

            item.innerHTML = `
                <div>
                    <strong>${user.name || '-'}</strong>
                </div>

                <div>
                    📧 ${user.email || '-'}
                </div>

                <div>
                    📱 ${user.mobile || '-'}
                </div>

                <div>
                    📍 ${user.address || '-'}
                </div>
            `;

            container.appendChild(item);

        });

    } catch (error) {

        console.error("Users Error:", error);

        alert("Failed to load users");

    }

}