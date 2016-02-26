require "resque"

class PythonReviewJob
  @queue = :python_review

  def self.perform(attributes)
    p attributes
    # filename
    # commit_sha
    # pull_request_number (pass-through)
    # patch (pass-through)
    # content
    # config

    violations = [{
      line: 1,
      message: "Hello from Docker!",
    }]

    Resque.enqueue(
      CompletedFileReviewJob,
      filename: attributes.fetch("filename"),
      commit_sha: attributes.fetch("commit_sha"),
      pull_request_number: attributes.fetch("pull_request_number"),
      patch: attributes.fetch("patch"),
      violations: violations,
    )
  end
end
