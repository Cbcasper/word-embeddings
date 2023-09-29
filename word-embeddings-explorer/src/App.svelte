<script>
    import axios from "axios";

    import Article from "./lib/Article.svelte";
    import Articles from "./lib/Articles.svelte";
    import ControlPanel from "./lib/ControlPanel.svelte";

    let selectedArticle;
    let loadArticles = () => axios.get("http://127.0.0.1:5000/articles");
    let select = event => selectedArticle = event.detail;
</script>

<main class="w-screen h-screen flex">
    {#await loadArticles() then data}
        <div class="flex-none w-1/3 max-w-md h-full overflow-scroll">
            <Articles articles={data.data} on:select={select}></Articles>
        </div>
    {/await}
    <div class="grow max-w-2/3 h-full">
        <Article article={selectedArticle}></Article>
        <ControlPanel article={selectedArticle}></ControlPanel>
    </div>
</main>
