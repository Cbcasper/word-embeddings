<script>
    import { tick } from "svelte";

    import Article from "./lib/Article.svelte";
    import Articles from "./lib/Articles.svelte";
    import Ranking from "./lib/Ranking.svelte";
    import ControlPanel from "./lib/ControlPanel.svelte";

    let article;
    let parameters;
    let updateRanking;

    async function select()
    {
        await tick();
        updateRanking(article, parameters);
    }
</script>

<main class="w-screen h-screen flex">
    <div class="flex-none w-1/3 max-w-md h-full overflow-scroll">
        <Articles bind:selectedArticle={article} on:select={select}></Articles>
    </div>
    <div class="grow max-w-2/3 h-full divide-y-2 divide-sky-800">
        <div class="h-1/2">
            <Ranking bind:update={updateRanking}></Ranking>
        </div>
        <div class="h-1/2 flex divide-x-2 divide-sky-800">
            <ControlPanel bind:parameters on:select={select}></ControlPanel>
            <Article {article}></Article>
        </div>
    </div>
</main>
