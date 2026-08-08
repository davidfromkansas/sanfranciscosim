// The concierge panel. It knows nothing about the scene: it posts the
// conversation plus a sanitized viewer state to /api/agent, applies whatever
// intents come back through the callback it was given, and then prints the
// answer. With no key configured the endpoint replies 503 and the panel says so
// once, rather than retrying.

const ENDPOINT = '/api/agent';

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

export function createConcierge({ viewerContext, applyIntent }) {
  const panel = el('div', 'toy-card');
  panel.id = 'concierge';
  panel.hidden = true;

  const head = el('div');
  head.id = 'concierge-head';
  head.append(el('span', null, 'City concierge'));
  const close = el('button', 'icon-button', '×');
  close.type = 'button';
  close.title = 'Close';
  close.style.marginLeft = 'auto';
  head.append(close);

  const log = el('div');
  log.id = 'concierge-log';

  const form = el('form');
  form.id = 'concierge-form';
  const input = el('input');
  input.id = 'concierge-input';
  input.placeholder = 'Ask about the city…';
  input.setAttribute('aria-label', 'Ask the city concierge');
  const send = el('button', 'toy-button', 'Ask');
  send.type = 'submit';
  form.append(input, send);

  panel.append(head, log, form);

  const toggle = el('button', 'toy-button', 'Ask the city');
  toggle.id = 'concierge-toggle';
  toggle.type = 'button';
  toggle.dataset.tone = 'teal';

  document.body.append(panel, toggle);

  const history = [];
  let busy = false;

  function append(role, text) {
    const bubble = el('div', 'msg', text);
    bubble.dataset.role = role;
    log.append(bubble);
    log.scrollTop = log.scrollHeight;
    return bubble;
  }

  function open() {
    panel.hidden = false;
    toggle.hidden = true;
    input.focus();
  }

  function hide() {
    panel.hidden = true;
    toggle.hidden = false;
  }

  close.addEventListener('click', hide);
  toggle.addEventListener('click', open);
  input.addEventListener('keydown', (event) => event.stopPropagation());
  input.addEventListener('keyup', (event) => event.stopPropagation());

  async function ask(question) {
    const text = question.trim();
    if (!text || busy) return;
    open();
    busy = true;
    input.value = '';
    append('user', text);
    history.push({ role: 'user', content: text });
    const pending = append('assistant', '…');

    try {
      const res = await fetch(ENDPOINT, {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ messages: history.slice(-12), context: viewerContext() }),
      });
      if (res.status === 503) {
        pending.dataset.role = 'error';
        pending.textContent =
          'The concierge is offline: this deployment has no AI gateway key. Clicking, search and everything else still works.';
        history.pop();
        return;
      }
      const body = await res.json();
      if (!res.ok) {
        pending.dataset.role = 'error';
        pending.textContent = body.error || `Request failed (${res.status}).`;
        history.pop();
        return;
      }
      // Intents move the view first, so the answer lands on the right picture.
      for (const intent of body.intents || []) {
        try {
          await applyIntent(intent);
        } catch (error) {
          console.warn('intent failed', intent, error);
        }
      }
      pending.textContent = body.text || 'No answer came back.';
      history.push({ role: 'assistant', content: body.text || '' });
    } catch (error) {
      pending.dataset.role = 'error';
      pending.textContent = `Could not reach the concierge: ${error.message}`;
      history.pop();
    } finally {
      busy = false;
    }
  }

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    ask(input.value);
  });

  return { ask, open, hide };
}
