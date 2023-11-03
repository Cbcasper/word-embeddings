<script>
    import Article from "./lib/Article.svelte";
    import Results from "./lib/Results.svelte";
    import Articles from "./lib/Articles.svelte";
    import ControlPanel from "./lib/ControlPanel.svelte";

    import { writable } from "svelte/store";

    const article = writable();
    const parameters = writable();
</script>

<main class="w-screen h-screen divide-y-2 divide-sky-800">
    <div class="w-full h-1/2 flex divide-x-2 divide-sky-800">
        <div class="max-w-md">
            <Articles {article}></Articles>
        </div>
        <Article {article}></Article>
        <ControlPanel {parameters}></ControlPanel>
    </div>
    <div class="h-1/2">
        <Results {article} {parameters}></Results>
    </div>
</main>
