<script>
    import axios from "axios";
    import { createEventDispatcher } from "svelte";

    export let article;

    const dispatch = createEventDispatcher();

    let loadArticles = () => axios.get("http://127.0.0.1:5000/articles");
    function select(selectedArticle)
    {
        article.set(selectedArticle);
        dispatch('select');
    }
</script>

<div class="divide-y divide-sky-100 border-r-2 border-l-8 border-sky-800">
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