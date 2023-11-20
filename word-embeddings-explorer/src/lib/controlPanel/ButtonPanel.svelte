<script>
    import { createEventDispatcher, onMount } from "svelte";

    export let options;
    export let selected;

    const dispatch = createEventDispatcher();

    function select(option)
    {
        selected = option;
        dispatch("select");
    }
    onMount(() => { select(options[0]); });
</script>

<ul class="text-right divide-y divide-sky-800 overflow-scroll snap-y">
    {#each options as option}
        <li class="snap-center">
            <button class:hover:bg-slate-200={selected !== option} class:bg-slate-300={selected === option}
                    class="p-2 w-full text-right" on:click={() => select(option)}>
                {option}
            </button>
        </li>
    {/each}
</ul>