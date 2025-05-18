const dryRun = (process.env.RELEASE_DRY_RUN || "false").toLowerCase() === "true";

const config = require('semantic-release-preconfigured-conventional-commits');

if (!dryRun) {
    config.plugins.push(
        ["@semantic-release/github", {
            assets: [
                { path: "dist/*" },
            ]
        }],
        ["@semantic-release/git", {
            assets: [
                "CHANGELOG.md",
                "pyproject.toml"
            ],
            message: "chore(release): ${nextRelease.version} [skip ci]\n\n${nextRelease.notes}"
        }]
    );
}

module.exports = config;