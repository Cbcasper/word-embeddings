<script>
    export let article;
</script>

<div class="px-4 pt-4 h-full flex flex-col">
    {#if article !== undefined}
        <div class="text-2xl border-b-2 border-sky-600">{article.title}</div>
        {#if article.subTitle !== null}
            <div class="text-xl">{article.subTitle}</div>
        {/if}
        <div class="grow pt-2 overflow-scroll text-ellipsis">
            {article.content}
        </div>
    {:else}
        <div class="font-bold">
            Select an article to begin
        </div>
    {/if}
</div>