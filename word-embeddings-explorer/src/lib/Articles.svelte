<script>
    import axios from "axios";

    export let article;

    function loadArticles()
    {
        let url = "http://127.0.0.1:5000/dataset";
        let config = { params: { dataset: "unlabeled" } };
        return axios.get(url, config);
    }
    function select(selectedArticle)
    {
        article.set(selectedArticle);
    }
</script>

<div class="h-full w-full divide-y divide-sky-100 border-l-8 border-sky-800 overflow-scroll">
    {#await loadArticles() then data}
        {#each data.data as listedArticle}
            <button class:bg-slate-300={$article === listedArticle.article}
                    class="w-full px-2 py-0.5 text-ellipsis text-left whitespace-nowrap overflow-hidden
                        hover:bg-slate-200"
                    on:click={() => select(listedArticle.article)}>
                {listedArticle.article.title}
            </button>
        {/each}
    {/await}
</div>