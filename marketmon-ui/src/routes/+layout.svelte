<script>
    import "../app.css";
</script>

<slot />
<style lang="postcss">
  :global(html) {
    background-color: theme(colors.gray.400);
  }
</style>
