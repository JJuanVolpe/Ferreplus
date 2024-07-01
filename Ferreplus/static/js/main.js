const getOptionChart = async (url) => {
    try {
        const response = await fetch(url);
        return await response.json();
    } catch (ex) {
        alert(ex);
    }
};

const initChart = async (chartId, url) => {
    const myChart = echarts.init(document.getElementById(chartId));
    myChart.setOption(await getOptionChart(url));
    myChart.resize();
};

const initAllCharts = async () => {
    await initChart("chart", "http://127.0.0.1:8000/get_chart/");
    await initChart("sucursales_chart", "http://127.0.0.1:8000/get_sucursales_chart/");
};

window.addEventListener("load", async () => {
    await initAllCharts();
    setInterval(async () => {
        await initAllCharts();
    }, 2000);
});