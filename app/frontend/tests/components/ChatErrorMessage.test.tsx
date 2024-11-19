// ChatErrorMessage.test.tsx
import { render, screen } from "@testing-library/react";
import { ChatErrorMessage } from "../../src/components/ChatErrorMessage";

describe("ChatErrorMessage", () => {
  it("renders the correct message in code font", () => {
    const errorMessage = "An unexpected error occurred.";

    render(<ChatErrorMessage error={errorMessage} />);

    const errorElement = screen.getByText(errorMessage);
    expect(errorElement).toBeInTheDocument();
    expect(errorElement).toHaveStyle({
      fontFamily: "var(--code-font-family)",
    });
  });
});
