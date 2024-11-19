import { fireEvent, render, screen } from "@testing-library/react";
import { ChatInput } from "../../src/components/ChatInput";

describe("ChatInput", () => {
  it("renders a text input area", () => {
    render(
      <ChatInput
        query=""
        setQuery={vi.fn()}
        onPressEnter={vi.fn()}
        leftFunctionalComponents={[]}
        rightFunctionalComponents={[]}
      />,
    );

    const inputElement = screen.getByRole("textbox");
    expect(inputElement).toBeInTheDocument();
  });

  it("renders left and right functional components", () => {
    render(
      <ChatInput
        query=""
        setQuery={vi.fn()}
        onPressEnter={vi.fn()}
        leftFunctionalComponents={[<button>Left</button>]}
        rightFunctionalComponents={[<button>Right</button>]}
      />,
    );

    expect(screen.getByText("Left")).toBeInTheDocument();
    expect(screen.getByText("Right")).toBeInTheDocument();
  });

  it("focuses the text area when any part is clicked", () => {
    const { container } = render(
      <ChatInput
        query=""
        setQuery={vi.fn()}
        onPressEnter={vi.fn()}
        leftFunctionalComponents={[]}
        rightFunctionalComponents={[]}
      />,
    );

    fireEvent.click(container.firstChild!);
    const inputElement = screen.getByRole("textbox");
    expect(inputElement).toHaveFocus();
  });

  it("updates the query when typing", () => {
    const mockSetQuery = vi.fn();

    render(
      <ChatInput
        query=""
        setQuery={mockSetQuery}
        onPressEnter={vi.fn()}
        leftFunctionalComponents={[]}
        rightFunctionalComponents={[]}
      />,
    );

    const textArea = screen.getByRole("textbox");
    fireEvent.change(textArea, { target: { value: "Hello, world!" } });
    expect(mockSetQuery).toHaveBeenCalledWith("Hello, world!");
  });

  it("calls onPressEnter when Enter is pressed without Shift", () => {
    const mockOnPressEnter = vi.fn();

    render(
      <ChatInput
        query=""
        setQuery={vi.fn()}
        onPressEnter={mockOnPressEnter}
        leftFunctionalComponents={[]}
        rightFunctionalComponents={[]}
      />,
    );

    const textArea = screen.getByRole("textbox");

    // Shift+Enter does not trigger onPressEnter
    fireEvent.keyDown(textArea, { key: "Enter", shiftKey: true });
    expect(mockOnPressEnter).not.toHaveBeenCalled();

    fireEvent.keyDown(textArea, { key: "Enter", shiftKey: false });
    expect(mockOnPressEnter).toHaveBeenCalledTimes(1);
  });
});
