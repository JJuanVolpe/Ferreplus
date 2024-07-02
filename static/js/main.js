const getOptionChart = async (url) => {
    try {
        const response = await fetch(url);
        const data = await response.json();
        console.log('Data fetched from URL:', url, data);
        return data;
    } catch (ex) {
        alert(ex);
    }
};

const initChart = async (chartId, url) => {
    const chartElement = document.getElementById(chartId);
    console.log(`Initializing chart with ID: ${chartId}`);
    if (chartElement) {
        console.log('Chart element found:', chartElement);
        const myChart = echarts.init(chartElement);
        const options = await getOptionChart(url);
        console.log('Setting options:', options);
        myChart.setOption(options);
        myChart.resize();
    } else {
        console.error(`Element with ID '${chartId}' not found.`);
    }
};

const initAllCharts = async () => {
    await initChart("chart", "http://127.0.0.1:8000/get_chart/");
    await initChart("sucursales_chart", "http://127.0.0.1:8000/get_sucursales_chart/");
    await initChart("intercambios_chart", "http://127.0.0.1:8000/get_intercambios_chart/");
};

window.addEventListener("load", async () => {
    console.log('Window loaded, initializing charts...');
    await initAllCharts();
    setInterval(async () => {
        console.log('Reinitializing charts...');
        await initAllCharts();
    }, 2000);
});