document.addEventListener("DOMContentLoaded", function () {

    const canvas = document.getElementById("performanceChart");

    if (!canvas) {
        return;
    }

    const ctx = canvas.getContext("2d");

    new Chart(ctx, {
        type: "bar",

        data: {
            labels: [
                "Excellent",
                "Very Good",
                "Good",
                "Average",
                "Risk"
            ],

            datasets: [{
                label: "Students",

                data: [
                    10,
                    20,
                    15,
                    8,
                    5
                ]
            }]
        },

        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true
                }
            }
        }
    });

});
