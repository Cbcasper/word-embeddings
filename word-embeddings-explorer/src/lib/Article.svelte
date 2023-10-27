<script>
    import MdEdit from "svelte-icons/md/MdEdit.svelte";
    import MdCheck from "svelte-icons/md/MdCheck.svelte";

    export let article;
    
    let displayArticle;
    
    let editing = false;
    let hovering = false;
    
    function update(updateValue)
    {
        displayArticle = updateValue;
        editing = false;
    }
    article.subscribe(update);

    let updateContent = event => { displayArticle.content = event.target.value; };
    function edit()
    {
        editing = true;
        displayArticle = { content: "", title: "Write your own article!" };
    }

    function submit()
    {
        article.set(displayArticle);
        editing = true;
    }
</script>

<article class="h-full grow pt-4 px-4 flex flex-col relative"
        on:mouseenter={() => hovering = true} on:mouseleave={() => hovering = false}>
    {#if displayArticle !== undefined}
        <div class="pb-2 text-2xl border-b-2 border-sky-600">{displayArticle.title}</div>
        {#if !editing}
            {#if displayArticle.subTitle !== null}
                <div class="text-xl">{displayArticle.subTitle}</div>
            {/if}
            <div class="grow py-2 overflow-scroll text-ellipsis">
                {displayArticle.content}
            </div>
        {:else}
            <textarea class="grow my-2 p-2 focus:outline-dashed focus:outline-2 focus:outline-sky-600 rounded-md"
                    placeholder="Start writing!" on:input={updateContent}></textarea>
        {/if}
    {:else}
        <div class="font-bold">
            Select an article to begin
        </div>
    {/if}
    <button class="pt-1 pr-1 pb-2 pl-2 w-10 h-10 absolute top-0 right-0 bg-white
                border-b-2 border-l-2 rounded-bl-md border-sky-800 text-sky-800"
            class:hidden={!(hovering && !editing)} on:click={edit}>
        <MdEdit/>
    </button>
    <button class="pt-1 pr-1 pb-2 pl-2 w-10 h-10 absolute top-0 right-0 bg-white
                border-b-2 border-l-2 rounded-bl-md border-sky-800 text-sky-800"
            class:hidden={!(hovering && editing)} on:click={submit}>
        <MdCheck/>
    </button>
</article>