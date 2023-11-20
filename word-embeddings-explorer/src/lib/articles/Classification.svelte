<script>
    export let title;
    export let field;
    export let styling;
</script>

{#if field !== undefined}
    <div class={styling}>
        <div class="text-lg">
            {title}
        </div>
        <div class="text-right">
            {field}
        </div>
    </div>
{/if}