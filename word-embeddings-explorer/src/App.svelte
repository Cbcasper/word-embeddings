<script>
    import Article from "./lib/Article.svelte";
    import Articles from "./lib/Articles.svelte";
    import Ranking from "./lib/Ranking.svelte";
    import ControlPanel from "./lib/ControlPanel.svelte";

    import { writable } from "svelte/store";

    const article = writable();
    const parameters = writable();
</script>

<main class="w-screen h-screen flex">
    <div class="flex-none w-1/3 max-w-md h-full overflow-scroll">
        <Articles {article}></Articles>
    </div>
    <div class="grow max-w-2/3 h-full divide-y-2 divide-sky-800">
        <div class="h-1/2">
            <Ranking {article} {parameters}></Ranking>
        </div>
        <div class="h-1/2 flex divide-x-2 divide-sky-800">
            <ControlPanel {parameters}></ControlPanel>
            <Article {article}></Article>
        </div>
    </div>
</main>
