# project

## Setup

### Initializing the Submodule

After cloning this repository, you need to initialize and update the submodule:

```bash
git submodule update --init --recursive
```

### Using a Specific Tag

To configure the submodule to use a specific tag (e.g., v0.7.2-dev3):

1. Navigate to the submodule directory:
   ```bash
   cd laser-measles
   ```

2. Checkout the desired tag:
   ```bash
   git checkout v0.7.2-dev3
   ```

3. Return to the project root and commit the submodule reference:
   ```bash
   cd ..
   git add laser-measles
   git commit -m "Update submodule to v0.7.2-dev3"
   ```

### Updating the Submodule

To update the submodule to the latest commit on its default branch:

```bash
git submodule update --remote laser-measles
```